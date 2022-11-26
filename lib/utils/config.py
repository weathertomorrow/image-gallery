import re
import os

from typing import cast, List, Union, Callable
from modules.shared import Options

from lib.config import RuntimeConfig, StaticConfig, ConfigurableConfig, TabConfig, BaseTabConfig

from lib.utils.int import strToNullableInt
from lib.utils.guards import isNotEmpty, isEmpty
from lib.utils.str import withPrefix

def getRuntimeConfig(opts: Options, staticConfig: StaticConfig, defaultConfig: ConfigurableConfig) -> RuntimeConfig:
  configAsDict = { key: opts.__getattr__(getConfigFieldId(staticConfig, key)) for key in defaultConfig.keys() }
  return cast(RuntimeConfig, configAsDict)

def getConfigFieldId(staticConfig: StaticConfig, fieldName: str) -> str:
  return withPrefix(staticConfig["extension_id"], fieldName)

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

  return dict(map(getLimit, config["max_tabs_sizes"].split(",")))

PathGetter = Callable[[str], str]

def makeGetCustomTabPath(config: RuntimeConfig) -> PathGetter:
  def getCustomTabPath(tabName: str) -> str:
    return os.path.join(config["root"], tabName)

  return getCustomTabPath

def makeGetBuiltinTabPath(config: StaticConfig) -> PathGetter:
  def getBuiltinTabPath(tabName: str) -> str:
    return config["builtinTabs"][tabName]

  return getBuiltinTabPath

def makeGenerateTabConfig(limits: TabSizeLimits, pathGetter: PathGetter):
  def generateTabConfig(tabName: str) -> BaseTabConfig:
    tabId = getTabId(tabName)
    return {
      "displayName": tabName,
      "id": tabId,
      "maxSize": limits[tabId] if tabId in limits else None,
      "path": pathGetter(tabName)
    }

  return generateTabConfig

def makeExpandTabConfig(runtimeConfig: RuntimeConfig, staticConfig: StaticConfig):
  def expandTabConfig(tabConfig: BaseTabConfig) -> TabConfig:
    return {
      **tabConfig,
      "runtimeConfig": runtimeConfig,
      "staticConfig": staticConfig,
    }

  return expandTabConfig

def getTabConfigs(config: RuntimeConfig, staticConfig: StaticConfig, tabs: List[str], pathGetter: PathGetter) -> List[TabConfig]:
  return list(
    map(makeExpandTabConfig(config, staticConfig),
      map(makeGenerateTabConfig(getTabLimits(config), pathGetter), tabs)
    )
  )

def getCustomTabsConfigs(config: RuntimeConfig, staticConfig: StaticConfig) -> List[TabConfig]:
  return getTabConfigs(
    config,
    staticConfig,
    list(filter(isNotEmpty, map(normalizeTabName, config["tabs"].split(',')))),
    makeGetCustomTabPath(config)
  )

def getBuiltinTabsConfig(config: RuntimeConfig, staticConfig: StaticConfig) -> List[TabConfig]:
  return getTabConfigs(
    config,
    staticConfig,
    list(staticConfig["builtinTabs"].keys()),
    makeGetBuiltinTabPath(staticConfig)
  )
