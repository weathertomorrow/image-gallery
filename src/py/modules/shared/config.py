import re
import os

from typing import cast, List, Union, Callable, TypedDict
from modules.shared import Options

from src.py.config import RuntimeConfig, StaticConfig, ConfigurableConfig, BaseTabConfig, GlobalConfig, SingleTabConfig, TabConfig

from src.py.modules.shared.int import strToNullableInt
from src.py.modules.shared.guards import isNotEmpty, isEmpty
from src.py.modules.shared.str import withPrefix

def getRuntimeConfig(opts: Options, staticConfig: StaticConfig, defaultConfig: ConfigurableConfig) -> RuntimeConfig:
  configAsDict = cast(RuntimeConfig, { key: opts.__getattr__(getConfigFieldId(staticConfig, key)) for key in defaultConfig.keys() })

  # ¯\_(ツ)_/¯
  configAsDict["pageColumns"] = int(configAsDict["pageColumns"])
  configAsDict["pageRows"] = int(configAsDict["pageRows"])
  configAsDict["preloadPages"] = int(configAsDict["preloadPages"])

  return cast(RuntimeConfig, configAsDict)

def getGlobalConfig(runtimeConfig: RuntimeConfig, staticConfig: StaticConfig) -> GlobalConfig:
  return {
    "runtimeConfig": runtimeConfig,
    "staticConfig": staticConfig
  }

def getConfigFieldId(staticConfig: StaticConfig, fieldName: str) -> str:
  return withPrefix(staticConfig["extensionId"], fieldName)

def normalizeTabName(tabName: str) -> str:
  return tabName.lower().strip().capitalize()

def getTabId(tabName: str) -> str:
  return re.sub(r'\s', "_", normalizeTabName(tabName).lower())

TabSizeLimits = dict[str, Union[int, None]];

def getTabLimits(config: RuntimeConfig) -> TabSizeLimits:
  def getLimit(configPair: str) -> tuple[str, Union[int, None]]:
    if isEmpty(configPair) or configPair.count(":") != 1:
      # ideally would return none, but python doesn't have actual type guards,
      # so instead return something that should never be accessed
      return ("dontcallatablikethisoritwillgetoverwritten", None)

    tabName, limit = configPair.split(":")
    return (getTabId(tabName), strToNullableInt(limit))

  return dict(map(getLimit, config["maxTabsSizes"].split(",")))

PathGetter = Callable[[str, str], str]

def makeGetCustomTabPath(config: RuntimeConfig) -> PathGetter:
  def getCustomTabPath(tabName: str, tabId: str) -> str:
    return os.path.join(config["root"], tabId)

  return getCustomTabPath

def makeGetBuiltinTabPath(config: StaticConfig) -> PathGetter:
  def getBuiltinTabPath(tabName: str, tabId: str) -> str:
    return config["builtinTabs"][tabName]["path"]

  return getBuiltinTabPath

FlagGetter = Callable[[str, str], bool]

class TabConfigGetters(TypedDict):
  path: PathGetter
  moveToEnabled: FlagGetter
  sendToEnabled: FlagGetter

def makeGenerateTabConfig(globalConfig: GlobalConfig, getters: TabConfigGetters):
  limits = getTabLimits(globalConfig["runtimeConfig"])

  def generateTabConfig(tabName: str) -> BaseTabConfig:
    tabId = getTabId(tabName)
    return {
      "displayName": tabName,
      "id": tabId,
      "maxSize": limits[tabId] if tabId in limits else None,
      "path": getters["path"](tabName, tabId),
      "thumbnailsPath": getters["path"](tabName, tabId) + globalConfig["staticConfig"]["thumbnails"]["folderSuffix"],
      "moveToEnabled": getters["moveToEnabled"](tabName, tabId),
      "sendToEnabled": getters["sendToEnabled"](tabName, tabId),
    }

  return generateTabConfig

def makeExpandTabConfig(globalConfig: GlobalConfig):
  def expandTabConfig(tabConfig: BaseTabConfig) -> SingleTabConfig:
    return {
      **tabConfig,
      **globalConfig,
    }

  return expandTabConfig

def getTabConfigs(globalConfig: GlobalConfig, tabs: List[str], getters: TabConfigGetters) -> List[SingleTabConfig]:
  return list(
    map(makeExpandTabConfig(globalConfig),
      map(makeGenerateTabConfig(globalConfig, getters), tabs)
    )
  )

def getCustomTabsConfigs(globalConfig: GlobalConfig) -> List[SingleTabConfig]:
  return getTabConfigs(
    globalConfig,
    list(filter(isNotEmpty, map(normalizeTabName, globalConfig["runtimeConfig"]["tabs"].split(',')))),
    {
      "path": makeGetCustomTabPath(globalConfig["runtimeConfig"]),
      "moveToEnabled": lambda _, __: True, # all custom tabs are allowed to be moved into,
      "sendToEnabled": lambda _, __: False # all custom tabs are not allowed to be sent into
    }

  )

def getBuiltinTabsConfig(globalConfig: GlobalConfig) -> List[SingleTabConfig]:
  return getTabConfigs(
    globalConfig,
    list(globalConfig["staticConfig"]["builtinTabs"].keys()),
    {
      "path": makeGetBuiltinTabPath(globalConfig["staticConfig"]),
      "moveToEnabled": lambda tabName, tabId: globalConfig["staticConfig"]["builtinTabs"][tabName]["moveToEnabled"],
      "sendToEnabled": lambda tabName, tabId: globalConfig["staticConfig"]["builtinTabs"][tabName]["sendToEnabled"],
    }
  )

def makeAreDifferentTabs(tab: SingleTabConfig):
  def areDifferentTabs(otherTab: SingleTabConfig):
    return tab["id"] != otherTab["id"]

  return areDifferentTabs

def mergeTabConfigs(tabConfigsA: List[SingleTabConfig], tabConfigsB: List[SingleTabConfig]) -> List[TabConfig]:
  everyTab = [*tabConfigsA, *tabConfigsB]
  tabsDict = { tab["id"]: tab for tab in everyTab}

  return [ { **tab, "otherTabs": list(filter(makeAreDifferentTabs(tab), everyTab)) } for (id, tab) in tabsDict.items()]
