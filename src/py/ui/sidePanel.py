import gradio
from typing import TypedDict

from src.py.config import TabConfig
from src.py.sort import SortBy, SortOrder

class ImageInfo(TypedDict):
  prompts: gradio.Textbox
  name: gradio.Textbox
  creationTime: gradio.HTML

class SidePanel(TypedDict):
  sortBy: gradio.Radio
  sortOrder: gradio.Radio
  searchBox: gradio.Textbox
  image: ImageInfo

def createSidePanel(tabConfig: TabConfig) -> SidePanel:
  with gradio.Column():
    with gradio.Row():
      sortBy = gradio.Radio(value = tabConfig["staticConfig"]["tabDefaults"]["sortBy"].value, choices = [opt.value for opt in SortBy] , label = "sort by", interactive = True)
      sortOrder = gradio.Radio(value = tabConfig["staticConfig"]["tabDefaults"]["sortOrder"].value, choices = [opt.value for opt in SortOrder], label = "sort order", interactive = True)
      searchBox = gradio.Textbox(label = "search by name")
    with gradio.Row():
      with gradio.Column():
        imgPrompts = gradio.Textbox(label = "Generated Info", interactive = False, lines = 6)
        imgName = gradio.Textbox(label = "File Name", interactive = False)
        imgTime = gradio.HTML()

  return  {
    "sortBy": sortBy,
    "sortOrder": sortOrder,
    "searchBox": searchBox,
    "image": {
      "prompts": imgPrompts,
      "name": imgName,
      "creationTime": imgTime
    }
  }
