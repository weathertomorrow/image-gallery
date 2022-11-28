import gradio

from modules.script_callbacks import on_ui_settings, on_ui_tabs
from modules.shared import opts, OptionInfo

from src.py.config import defaultConfigurableConfig, staticConfig, uiLabelsConfig
from src.py.utils.str import withSuffix
from src.py.utils.config import getRuntimeConfig, getCustomTabsConfigs, getBuiltinTabsConfig, getConfigFieldId, getGlobalConfig, mergeTabConfigs
from src.py.tabs import createTab

def setup_tabs():
  globalConfig = getGlobalConfig(getRuntimeConfig(opts, staticConfig, defaultConfigurableConfig), staticConfig)
  defaultTabConfigs = getBuiltinTabsConfig(globalConfig)
  customTabConfigs = getCustomTabsConfigs(globalConfig)

  # merge configs to avoid duplicates
  tabs = mergeTabConfigs(defaultTabConfigs, customTabConfigs)

  with gradio.Blocks(analytics_enabled = False) as gallery:
    with gradio.Tabs(elem_id = withSuffix(staticConfig["extensionId"], staticConfig["suffixes"]["extensionTab"])):
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
