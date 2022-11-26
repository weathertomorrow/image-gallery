import gradio

from modules.script_callbacks import on_ui_settings, on_ui_tabs
from modules.shared import opts, OptionInfo

from lib.config import defaultConfigurableConfig, staticConfig, uiLabelsConfig
from lib.utils.str import withSuffix
from lib.utils.config import getRuntimeConfig, getCustomTabsConfigs, getBuiltinTabsConfig, getConfigFieldId
from lib.tabs import createTab

def setup_tabs():
  runtimeConfig = getRuntimeConfig(opts, staticConfig, defaultConfigurableConfig)
  defaultTabConfigs = getBuiltinTabsConfig(runtimeConfig, staticConfig)
  customTabConfigs = getCustomTabsConfigs(runtimeConfig, staticConfig)

  # merge configs to avoid duplicates
  tabs = { tab["id"]: tab for tab in [*defaultTabConfigs, *customTabConfigs] }.values()

  with gradio.Blocks(analytics_enabled = False) as gallery:
    with gradio.Tabs(elem_id = withSuffix(staticConfig["suffixes"]["allTabs"], staticConfig["extension_id"])):
      for tab in tabs:
        createTab(tab)

  return (gallery, uiLabelsConfig["extension_name"], staticConfig["extension_id"]),

def setup_options():
  section = (staticConfig["extension_id"], uiLabelsConfig["extension_name"])

  for key in defaultConfigurableConfig.keys():
    opts.add_option(getConfigFieldId(staticConfig, key), OptionInfo(*defaultConfigurableConfig[key], section = section))


# calling code
on_ui_settings(setup_options)
on_ui_tabs(setup_tabs)
