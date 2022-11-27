import gradio
from typing import TypedDict

from src.py.config import TabConfig

class ImageInfo(TypedDict):
  prompts: gradio.Textbox
  name: gradio.Textbox
  creationTime: gradio.HTML

class SidePanel(TypedDict):
  sortBy: gradio.Radio
  searchBox: gradio.Textbox
  image: ImageInfo

def createSidePanel(tabConfig: TabConfig) -> SidePanel:
  with gradio.Column():
    with gradio.Row():
        sortBy = gradio.Radio(value = "date", choices = ["path name", "date"], label= "sort by" )
        searchBox = gradio.Textbox(label = "search by name")
    with gradio.Row():
        with gradio.Column():
            imgPrompts = gradio.Textbox(label = "Generated Info", interactive = False, lines=6)
            imgName = gradio.Textbox(label = "File Name", interactive = False)
            imgTime = gradio.HTML()

  return  {
    "sortBy": sortBy,
    "searchBox": searchBox,
    "image": {
      "prompts": imgPrompts,
      "name": imgName,
      "creationTime": imgTime
    }
  }
