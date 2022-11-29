import gradio
from typing import TypedDict

from src.py.config import TabConfig, SingleTabConfig
from src.py.modules.shared.str import withPrefix

from src.py.modules.tabs.logic.tabs import getTabElementId

class Buttons(TypedDict):
  deselect: gradio.Button
  moveTo: list[tuple[SingleTabConfig, gradio.Button]]

class ImageInfo(TypedDict):
  prompts: gradio.Textbox
  name: gradio.Textbox
  creationTime: gradio.HTML

class SidePanel(TypedDict):
  container: gradio.Column
  image: ImageInfo
  buttons: Buttons

def makeCreateMoveToButton(tabCofig: TabConfig):
  def createMoveToButton(otherTab: SingleTabConfig) -> tuple[SingleTabConfig, gradio.Button]:
    buttonId = getTabElementId(withPrefix(otherTab["id"], tabCofig["staticConfig"]["elementsSuffixes"]["moveToButton"]), tabCofig)
    return (otherTab, gradio.Button(elem_id = buttonId, value = f'Move to {otherTab["displayName"]}'))

  return createMoveToButton


def createSidePanel(tabConfig: TabConfig) -> SidePanel:
  createMoveToButton = makeCreateMoveToButton(tabConfig)

  with gradio.Column(visible = False) as container:
    with gradio.Column():
      imgPrompts = gradio.Textbox(label = "Generated Info", interactive = False, lines = 6)
      imgName = gradio.Textbox(label = "File Name", interactive = False, lines = 2)
      imgTime = gradio.HTML()
    with gradio.Column():
      with gradio.Row():
        moveTo = [createMoveToButton(otherTab) for otherTab in tabConfig["otherTabs"]]
      deselect = gradio.Button(value = "Close")

  return  {
    "container": container,
    "buttons": {
      "deselect": deselect,
      "moveTo": moveTo,
    },
    "image": {
      "prompts": imgPrompts,
      "name": imgName,
      "creationTime": imgTime
    }
  }
