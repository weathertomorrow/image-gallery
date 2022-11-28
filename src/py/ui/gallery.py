import gradio
from typing import TypedDict, List, Callable

from src.py.sort import SortBy, SortOrder
from src.py.utils.tabs import getTabElementId
from src.py.utils.str import withPrefix
from src.py.config import TabConfig

class Navigation(TypedDict):
  firstPage: gradio.Button
  prevPage: gradio.Button
  pageIndex: gradio.Number
  nextPage: gradio.Button
  lastPage: gradio.Button

class Sort(TypedDict):
  by: gradio.Radio
  order: gradio.Radio
  searchBox: gradio.Textbox

class Gallery(TypedDict):
  navigation: Navigation
  sort: Sort
  gallery: gradio.Box
  buttons: List[List[gradio.Button]]
  hiddenImagesSrcContainers: List[gradio.HTML]
  hiddenSelectedImage: gradio.Image

def makeCreateButton(tabConfig: TabConfig):
  suffixes = tabConfig["staticConfig"]["suffixes"]

  def createButton(column: int, row: int):
    button = gradio.Button(value = "", elem_id = getTabElementId(withPrefix(f'{column}_{row}', suffixes["imgButton"]), tabConfig))
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

class CreateGalleryArg(TypedDict):
  tabConfig: TabConfig
  getImagesPage: GetImagesPage

def createGallery(arg: CreateGalleryArg) -> Gallery:
  tabConfig = arg["tabConfig"]
  staticConfig = tabConfig["staticConfig"]
  suffixes = staticConfig["suffixes"]

  with gradio.Column(scale = 2):
    hiddenImagesSrcContainers = createSrcContainers(tabConfig, arg["getImagesPage"])
    hiddenSelectedImage = gradio.Image(visible = False, type = "pil")

    createButton = makeCreateButton(tabConfig)

    with gradio.Row():
      sortBy = gradio.Radio(value = tabConfig["staticConfig"]["tabDefaults"]["sortBy"].value, choices = [opt.value for opt in SortBy] , label = "sort by", interactive = True)
      sortOrder = gradio.Radio(value = tabConfig["staticConfig"]["tabDefaults"]["sortOrder"].value, choices = [opt.value for opt in SortOrder], label = "sort order", interactive = True)
      searchBox = gradio.Textbox(label = "search by name")

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
    "navigation": {
      "firstPage": firstPage,
      "prevPage": prevPage,
      "pageIndex": pageIndex,
      "nextPage": nextPage,
      "lastPage": lastPage,
    },
    "gallery": gallery,
    "buttons": buttons,
    "hiddenImagesSrcContainers": hiddenImagesSrcContainers,
    "hiddenSelectedImage": hiddenSelectedImage,
    "sort": {
      "by": sortBy,
      "order": sortOrder,
      "searchBox": searchBox,
    }
  }
