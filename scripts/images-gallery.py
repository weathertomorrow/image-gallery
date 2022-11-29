import gradio

from modules.script_callbacks import on_ui_settings, on_ui_tabs, on_image_saved
from modules.shared import opts, OptionInfo
from modules.generation_parameters_copypaste import bind_buttons

from src.py.config import defaultConfigurableConfig, staticConfig, uiLabelsConfig
from src.py.modules.shared.str import withSuffix
from src.py.modules.shared.config import getConfigFieldId, getGlobalConfig, getRuntimeConfig, getBuiltinTabsConfig, getCustomTabsConfigs, mergeTabConfigs

from src.py.modules.tabs.tabs import createTab
from src.py.modules.thumbnails.thumbnails import hadleMissingThumbnails
from src.py.modules.thumbnails.listeners import makeImageSavedListener


def setupTabs():
  globalConfig = getGlobalConfig(getRuntimeConfig(opts, staticConfig, defaultConfigurableConfig), staticConfig)
  defaultTabConfigs = getBuiltinTabsConfig(globalConfig)
  customTabConfigs = getCustomTabsConfigs(globalConfig)

  tabs = mergeTabConfigs(defaultTabConfigs, customTabConfigs)

  with gradio.Blocks(analytics_enabled = False) as gallery:
    if globalConfig["runtimeConfig"]["useThumbnails"]:
      hadleMissingThumbnails(tabs)

    with gradio.Tabs(elem_id = withSuffix(staticConfig["extensionId"], staticConfig["elementsSuffixes"]["extensionTab"])):
      for tab in tabs:
        bind_buttons(*createTab(tab)["sendToButtonsConfig"])
        on_image_saved(makeImageSavedListener(tab))

  return (gallery, uiLabelsConfig["extension_name"], staticConfig["extensionId"]),

def setupOptions():
  section = (staticConfig["extensionId"], uiLabelsConfig["extension_name"])

  for key in defaultConfigurableConfig.keys():
    opts.add_option(getConfigFieldId(staticConfig, key), OptionInfo(*defaultConfigurableConfig[key], section = section))

# calling code
on_ui_settings(setupOptions)
on_ui_tabs(setupTabs)
