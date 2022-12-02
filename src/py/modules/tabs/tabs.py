import gradio
from typing import TypedDict

from src.py.config import TabConfig
from src.py.modules.shared.files import makeDirIfMissing, removeDirIfExists
from src.py.modules.shared.mutable import getImagesInDirRef, makeWithRefreshFiles, addThumbnailsToImages, removeFilesOverLimit

from src.py.modules.tabs.ui.gallery import createGallery
from src.py.modules.tabs.ui.sidePanel import createSidePanel
from src.py.modules.tabs.ui.tabInfo import createTabInfo
from src.py.modules.tabs.ui.eventHandlers import makeOnImageClick, onImageChange, makeMoveImage, deselectImage, getEventInputsAndOutputs

from src.py.modules.tabs.logic.tabs import getTabElementId
from src.py.modules.tabs.logic.types import PageChangingFNConfig
from src.py.modules.tabs.logic.images import makeGetImages, getImagesPerPage, imagesIntoData
from src.py.modules.tabs.logic.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageAtIndex, getPageOffsets, makeRefreshPageForCounter

class CreateTabReturnValue(TypedDict):
  sendToButtonsConfig: tuple[dict[str, gradio.Button], gradio.Textbox, gradio.Textbox]

def createTab(tabConfig: TabConfig) -> CreateTabReturnValue:
  makeDirIfMissing(tabConfig["path"])
  if (tabConfig["runtimeConfig"]["useThumbnails"]):
    makeDirIfMissing(tabConfig["thumbnailsPath"])
  else:
    removeDirIfExists(tabConfig["thumbnailsPath"])

  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig["tabDefaults"]
  runtimeConfig = tabConfig["runtimeConfig"]

  allImagesInDirRef = removeFilesOverLimit(addThumbnailsToImages(getImagesInDirRef(tabConfig, tabConfig["path"]), tabConfig), tabConfig)
  getImages = makeGetImages(tabConfig, allImagesInDirRef)
  imagesPerPage = getImagesPerPage(tabConfig)
  withRefreshFiles = makeWithRefreshFiles(allImagesInDirRef, tabConfig)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig["elementsSuffixes"]["galleryTab"], tabConfig)):
    createTabInfo(tabConfig)
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery({
            "tabConfig": tabConfig,
            "getImagesPage": lambda index: imagesIntoData(getImages(index, defaults["sortOrder"], defaults["sortBy"])) if index >= 0 else '',
          })
          sidePanel = createSidePanel(tabConfig)


  inputsAndOutputs = getEventInputsAndOutputs(gallery, sidePanel)
  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'pageOffsets': getPageOffsets(runtimeConfig["preloadPages"]),
    'imagesPerPage': imagesPerPage,
    "imagesInDirRef": allImagesInDirRef
  }

  gallery["navigation"]["nextPage"].click(makeChangePage(changePageConfig, 1), **inputsAndOutputs["navigation"])
  gallery["navigation"]["prevPage"].click(makeChangePage(changePageConfig, -1), **inputsAndOutputs["navigation"])
  gallery["navigation"]["firstPage"].click(makeGoToFirstPage(changePageConfig), **inputsAndOutputs["navigation"])
  gallery["navigation"]["lastPage"].click(makeGoToLastPage(changePageConfig), **inputsAndOutputs["navigation"])
  gallery["navigation"]["pageIndex"].change(makeGoToPageAtIndex(changePageConfig), **inputsAndOutputs["navigation"])
  gallery["sort"]["by"].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs["navigation"])
  gallery["sort"]["order"].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs["navigation"])

  gallery["refreshButton"].click(withRefreshFiles(makeGoToPageAtIndex(changePageConfig)), **inputsAndOutputs["hiddenRefreshButton"])
  gallery["hidden"]["refreshCounter"].change(withRefreshFiles(makeRefreshPageForCounter(changePageConfig)), **inputsAndOutputs["hiddenRefreshCounter"])

  for (row, buttonRow) in enumerate(gallery["buttons"]):
    for (column, button) in enumerate(buttonRow):
      button.click(makeOnImageClick(tabConfig, column, row), **inputsAndOutputs["imageButton"])
  gallery["hidden"]["selectedImage"].change(onImageChange, **inputsAndOutputs["selectedImage"])

  for (otherTab, moveToOtherTabButton) in sidePanel["buttons"]["moveTo"]:
    moveToOtherTabButton.click(makeMoveImage(otherTab, allImagesInDirRef), **inputsAndOutputs["moveToTabButton"])
  sidePanel["buttons"]["deselect"].click(deselectImage, **inputsAndOutputs["deselectButton"])

  return {
    "sendToButtonsConfig": (
      sidePanel["buttons"]["sendTo"],
      sidePanel["image"]["name"],
      sidePanel["image"]["prompts"],
    )
  }
