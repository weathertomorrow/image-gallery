import gradio
from json import dumps
from typing import TypedDict

from src.py.config import TabConfig

from src.py.modules.tabs.logic.tabs import getTabElementId

class TabInfo(TypedDict):
  container: gradio.HTML

def createTabInfo(tabConfig: TabConfig) -> TabInfo:
  with gradio.Row(visible = False):
    tabInfo = dumps({
      "keybind": tabConfig['keybind']
    })

    container = gradio.HTML(value = tabInfo, elem_id = getTabElementId(tabConfig['staticConfig']['elementsSuffixes']['hiddenTabInfo'], tabConfig))

  return {
    "container": container,
  }
