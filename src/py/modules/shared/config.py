import re
from os import path

from typing import cast, List, Union, Callable, TypedDict
from modules.shared import Options

from src.py.config import RuntimeConfig, StaticConfig, ConfigurableConfig, BaseTabConfig, GlobalConfig, SingleTabConfig, TabConfig

from src.py.modules.shared.int import strToNullableInt
from src.py.modules.shared.guards import isNotEmpty, isEmpty
from src.py.modules.shared.str import withPrefix


StringGetter = Callable[[str], str]
FlagGetter = Callable[[str], bool]
TabSizeLimits = dict[str, Union[int, None]]
TabKeybinds = dict[str, str]

class TabConfigGetters(TypedDict):
  path: StringGetter
  moveToEnabled: FlagGetter
  sendToEnabled: FlagGetter

disallowedTabName = 'dontcallatablikethisoritwillgetoverwritten'

def getRuntimeConfig(opts: Options, staticConfig: StaticConfig, defaultConfig: ConfigurableConfig) -> RuntimeConfig:
  configAsDict = cast(RuntimeConfig, { key: opts.__getattr__(getConfigFieldId(staticConfig, key)) for key in defaultConfig.keys() })

  # ¯\_(ツ)_/¯
  configAsDict["pageColumns"] = int(configAsDict["pageColumns"])
  configAsDict["pageRows"] = int(configAsDict["pageRows"])
  configAsDict["preloadPages"] = int(configAsDict["preloadPages"])
  configAsDict["root"] = path.normpath(configAsDict["root"])

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

def getTabConfigPairs(configStr: str) -> list[tuple[str, str]]:
  def getPair(possiblePair: str) -> Union[tuple[str, str], None]:
    if isEmpty(possiblePair) or possiblePair.count(":") != 1:
      return None
    tabName, configValue = possiblePair.split(":")

    if (isEmpty(tabName) or isEmpty(configValue)):
      return None

    return (getTabId(tabName), configValue)
  return [pair for pair in map(getPair, configStr.split(',')) if pair is not None]

def getTabKeybinds(config: RuntimeConfig) -> TabKeybinds:
  return dict(getTabConfigPairs(config["tabKeybinds"]))

def getTabLimits(config: RuntimeConfig) -> TabSizeLimits:
  def getLimit(configPair: tuple[str, str]) -> tuple[str, Union[None, int]]:
    tabName, limit = configPair
    return (getTabId(tabName), strToNullableInt(limit))

  return dict(map(getLimit, getTabConfigPairs(config["maxTabsSizes"])))

def makeGetCustomTabPath(config: RuntimeConfig) -> StringGetter:
  def getCustomTabPath(tabId: str) -> str:
    return path.join(config["root"], tabId)

  return getCustomTabPath

def makeGetBuiltinTabPath(config: StaticConfig) -> StringGetter:
  def getBuiltinTabPath(tabId: str) -> str:
    return config["builtinTabs"][tabId]["path"]

  return getBuiltinTabPath

def makeGenerateTabConfig(globalConfig: GlobalConfig, getters: TabConfigGetters):
  limits = getTabLimits(globalConfig["runtimeConfig"])
  keybinds = getTabKeybinds(globalConfig["runtimeConfig"])

  def generateTabConfig(tabName: str) -> BaseTabConfig:
    tabId = getTabId(tabName)
    tabPath = path.normpath(getters["path"](tabId))
    thumbnailsPath = tabPath + globalConfig["staticConfig"]["thumbnails"]["folderSuffix"]

    return {
      "id": tabId,
      "displayName": tabName,
      "keybind": keybinds[tabId] if tabId in keybinds else None,
      "maxSize": limits[tabId] if tabId in limits else None,
      "path": tabPath,
      "thumbnailsPath": thumbnailsPath,
      "moveToEnabled": getters["moveToEnabled"](tabId),
      "sendToEnabled": getters["sendToEnabled"](tabId),
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
      "moveToEnabled": lambda _,: True, # all custom tabs are allowed to be moved into,
      "sendToEnabled": lambda _,: False # all custom tabs are not allowed to be sent into
    }

  )

def getBuiltinTabsConfig(globalConfig: GlobalConfig) -> List[SingleTabConfig]:
  return getTabConfigs(
    globalConfig,
    [tab["displayName"] for tab in globalConfig["staticConfig"]["builtinTabs"].values()],
    {
      "path": makeGetBuiltinTabPath(globalConfig["staticConfig"]),
      "moveToEnabled": lambda tabId: globalConfig["staticConfig"]["builtinTabs"][tabId]["moveToEnabled"],
      "sendToEnabled": lambda tabId: globalConfig["staticConfig"]["builtinTabs"][tabId]["sendToEnabled"],
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
