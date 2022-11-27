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
  hiddenImagesSrcContainers: List[gradio.HTML]

ImageClickHandler = Callable[[int, int], None]

def makeCreateButton(tabConfig: TabConfig, imageClickHandler: ImageClickHandler):
  suffixes = tabConfig["staticConfig"]["suffixes"]

  def createButton(column: int, row: int,):
    button = gradio.Button(value = "", elem_id = getTabElementId(withPrefix(f'{column}_{row}', suffixes["imgButton"]), tabConfig))
    button.click(lambda x = column, y = row: imageClickHandler(x, y))

    return button

  return createButton

GetImagesPage = Callable[[int], str]

def createSrcContainers(tabConfig: TabConfig, getImagesPage: GetImagesPage) -> List[gradio.HTML]:
  preloadPagesAmount = tabConfig["runtimeConfig"]["preloadPages"]
  suffixes = tabConfig["staticConfig"]["suffixes"]

  return [
    gradio.HTML(
        elem_id = getTabElementId(withPrefix(f'{pageIndex}', suffixes["imgSrcs"]), tabConfig),
        value = getImagesPage(pageIndex), visible = False)
    for
      pageIndex
    in range(0 - preloadPagesAmount, preloadPagesAmount + 1)
  ]

def createGallery(tabConfig: TabConfig, getImagesPage: GetImagesPage, imageClickHandler: ImageClickHandler) -> Gallery:
  staticConfig = tabConfig["staticConfig"]
  suffixes = staticConfig["suffixes"]
  createButton = makeCreateButton(tabConfig, imageClickHandler)

  with gradio.Column(scale = 2):
    hiddenImagesSrcContainers = createSrcContainers(tabConfig, getImagesPage)

    with gradio.Row():
      firstPage = gradio.Button('First Page')
      prevPage = gradio.Button('Prev Page')
      pageIndex = gradio.Number(value = staticConfig["tabDefaults"]["pageIndex"], label = "Page Index")
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
    "hiddenImagesSrcContainers": hiddenImagesSrcContainers,
  }
