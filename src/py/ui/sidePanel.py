import gradio
from typing import TypedDict

from src.py.config import TabConfig, SingleTabConfig
from src.py.utils.tabs import getTabElementId
from src.py.utils.str import withPrefix

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
    buttonId = getTabElementId(withPrefix(otherTab["id"], tabCofig["staticConfig"]["suffixes"]["moveToButton"]), tabCofig)
    return (otherTab, gradio.Button(elem_id = buttonId, value = f'Move to {otherTab["displayName"]}'))

  return createMoveToButton


def createSidePanel(tabConfig: TabConfig) -> SidePanel:
  createMoveToButton = makeCreateMoveToButton(tabConfig)

  with gradio.Column(visible = False) as container:
    with gradio.Column():
      imgPrompts = gradio.Textbox(label = "Generated Info", interactive = False, lines = 6)
      imgName = gradio.Textbox(label = "File Name", interactive = False)
      imgTime = gradio.HTML()
    with gradio.Column():
      deselect = gradio.Button(value = "Deselect")
      with gradio.Row():
        moveTo = [createMoveToButton(otherTab) for otherTab in tabConfig["otherTabs"]]

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
