import gradio

from modules.script_callbacks import on_ui_settings, on_ui_tabs
from modules.shared import opts, OptionInfo

from src.py.config import defaultConfigurableConfig, staticConfig, uiLabelsConfig
from src.py.modules.shared.str import withSuffix
from src.py.modules.shared.config import getConfigFieldId, getGlobalConfig, getRuntimeConfig, getBuiltinTabsConfig, getCustomTabsConfigs, mergeTabConfigs

from src.py.modules.tabs.tabs import createTab
from src.py.modules.thumbnails.thumbnails import hadleMissingThumbnails

def setup_tabs():
  globalConfig = getGlobalConfig(getRuntimeConfig(opts, staticConfig, defaultConfigurableConfig), staticConfig)
  defaultTabConfigs = getBuiltinTabsConfig(globalConfig)
  customTabConfigs = getCustomTabsConfigs(globalConfig)

  tabs = mergeTabConfigs(defaultTabConfigs, customTabConfigs)

  with gradio.Blocks(analytics_enabled = False) as gallery:
    if globalConfig["runtimeConfig"]["useThumbnails"]:
      hadleMissingThumbnails(tabs)

    with gradio.Tabs(elem_id = withSuffix(staticConfig["extensionId"], staticConfig["elementsSuffixes"]["extensionTab"])):
      for tab in tabs:
        createTab(tab)

  return (gallery, uiLabelsConfig["extension_name"], staticConfig["extensionId"]),

def setup_options():
  section = (staticConfig["extensionId"], uiLabelsConfig["extension_name"])

  for key in defaultConfigurableConfig.keys():
    opts.add_option(getConfigFieldId(staticConfig, key), OptionInfo(*defaultConfigurableConfig[key], section = section))

# calling code
on_ui_settings(setup_options)
on_ui_tabs(setup_tabs)
