import gradio
from typing import TypedDict, List, Callable

from src.py.config import TabConfig, SortBy, SortOrder
from src.py.modules.shared.str import withPrefix

from src.py.modules.tabs.logic.tabs import getTabElementId

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

class HiddenElements(TypedDict):
  imagesSrcContainers: List[gradio.HTML]
  selectedImage: gradio.Image
  refreshButton: gradio.Button #for refreshing files due to interaction outside of the tab
  refreshCounter: gradio.Number #for refreshing files due to interaction inside of the tab

class Gallery(TypedDict):
  navigation: Navigation
  sort: Sort
  gallery: gradio.Box
  buttons: List[List[gradio.Button]]
  hidden: HiddenElements


def makeCreateButton(tabConfig: TabConfig):
  suffixes = tabConfig["staticConfig"]["elementsSuffixes"]

  def createButton(column: int, row: int):
    button = gradio.Button(value = "", elem_id = getTabElementId(withPrefix(f'{column}_{row}', suffixes["imgButton"]), tabConfig))
    return button

  return createButton

GetImagesPage = Callable[[int], str]
def createSrcContainers(tabConfig: TabConfig, getImagesPage: GetImagesPage) -> List[gradio.HTML]:
  preloadPagesAmount = tabConfig["runtimeConfig"]["preloadPages"]
  suffixes = tabConfig["staticConfig"]["elementsSuffixes"]

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
  suffixes = staticConfig["elementsSuffixes"]

  with gradio.Column(scale = 2):
    with gradio.Row(visible = False):
      hiddenImagesSrcContainers = createSrcContainers(tabConfig, arg["getImagesPage"])
      hiddenSelectedImage = gradio.Image(visible = False, type = "pil")
      hiddenRefreshButton = gradio.Button(visible = False, elem_id = getTabElementId(tabConfig["staticConfig"]["elementsSuffixes"]["hiddenRefreshButton"], tabConfig))
      hiddenRefreshCounter = gradio.Number(visible = False, value = 0)

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
    "hidden": {
      "imagesSrcContainers": hiddenImagesSrcContainers,
      "selectedImage": hiddenSelectedImage,
      "refreshButton": hiddenRefreshButton,
      "refreshCounter": hiddenRefreshCounter,
    },
    "sort": {
      "by": sortBy,
      "order": sortOrder,
      "searchBox": searchBox,
    }
  }
