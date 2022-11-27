import gradio
from typing import TypedDict, List, Callable

from src.py.utils.tabs import getTabElementId
from src.py.utils.str import withPrefix
from src.py.config import TabConfig

class Gallery(TypedDict):
  firstPage: gradio.Button
  prevPage: gradio.Button
  pageIndex: gradio.Number
  nextPage: gradio.Button
  lastPage: gradio.Button
  gallery: gradio.Box
  buttons: List[List[gradio.Button]]
  hiddenImagesSrcContainer: gradio.HTML

ImageClickHandler = Callable[[int, int], None]

def makeCreateButton(tabConfig: TabConfig, imageClickHandler: ImageClickHandler) :
  suffixes = tabConfig["staticConfig"]["suffixes"]

  def createButton(column: int, row: int,):
    button = gradio.Button(value = "", elem_id = getTabElementId(withPrefix(f'{column}_{row}', suffixes["imgButton"]), tabConfig))
    button.click(lambda x = column, y = row: imageClickHandler(x, y))

    return button

  return createButton

def createGallery(tabConfig: TabConfig, initialImagesSrcs: str, imageClickHandler: ImageClickHandler) -> Gallery:
  staticConfig = tabConfig["staticConfig"]
  suffixes = staticConfig["suffixes"]
  createButton = makeCreateButton(tabConfig, imageClickHandler)

  with gradio.Column(scale = 2):
    hiddenImagesSrcContainer = gradio.HTML(elem_id = getTabElementId(suffixes["imgSrcs"], tabConfig), value = initialImagesSrcs, visible = False)

    with gradio.Row():
      firstPage = gradio.Button('First Page')
      prevPage = gradio.Button('Prev Page')
      pageIndex = gradio.Number(value = 0, label = "Page Index")
      nextPage = gradio.Button('Next Page')
      lastPage = gradio.Button('Last Page')

    with gradio.Box(elem_id = getTabElementId(suffixes["gallery"], tabConfig)) as gallery:
      with gradio.Box():
        with gradio.Box():
          buttons = list(
            map(lambda rowIndex:
              list(
                map(lambda columnIndex: createButton(columnIndex, rowIndex),
                range(0, tabConfig["runtimeConfig"]["pageColumns"]))
              ),
              range(0, tabConfig["runtimeConfig"]["pageRows"])
            )
          )

  return {
    "firstPage": firstPage,
    "prevPage": prevPage,
    "pageIndex": pageIndex,
    "nextPage": nextPage,
    "lastPage": lastPage,
    "gallery": gallery,
    "buttons": buttons,
    "hiddenImagesSrcContainer": hiddenImagesSrcContainer,
  }
