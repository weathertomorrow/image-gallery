import gradio

from src.py.config import TabConfig
from src.py.utils.tabs import getTabElementId
from src.py.logic.types import PageChangingFNConfig

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel
from src.py.ui.eventHandlers import makeOnImageClick, onImageChange, makeMoveImage, deselectImage, getEventInputsAndOutputs

from src.py.logic.files import makeDirIfMissing
from src.py.logic.mutable import getImagesInDirRef, makeWithRefreshFiles
from src.py.logic.images import makeGetImages, getImagesPerPage, imagesIntoData
from src.py.logic.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageAtIndex, getPageOffsets, makeRefreshPageForCounter

def createTab(tabConfig: TabConfig):
  makeDirIfMissing(tabConfig['path'])

  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig['tabDefaults']
  runtimeConfig = tabConfig["runtimeConfig"]

  allImagesInDirRef = getImagesInDirRef(tabConfig, staticConfig, tabConfig['path'])
  getImages = makeGetImages(tabConfig, allImagesInDirRef)
  imagesPerPage = getImagesPerPage(tabConfig)
  withRefreshFiles = makeWithRefreshFiles(allImagesInDirRef, staticConfig, tabConfig['path'])

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig['suffixes']['galleryTab'], tabConfig)):
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery({
            "tabConfig": tabConfig,
            "getImagesPage": lambda index: imagesIntoData(getImages(index, defaults['sortOrder'], defaults['sortBy'])) if index >= 0 else '',
          })
          sidePanel = createSidePanel(tabConfig)

  inputsAndOutputs = getEventInputsAndOutputs(gallery, sidePanel)
  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'pageOffsets': getPageOffsets(runtimeConfig['preloadPages']),
    'imagesPerPage': imagesPerPage,
    "imagesInDirRef": allImagesInDirRef
  }

  gallery['navigation']['nextPage'].click(makeChangePage(changePageConfig, 1), **inputsAndOutputs['navigation'])
  gallery['navigation']['prevPage'].click(makeChangePage(changePageConfig, -1), **inputsAndOutputs['navigation'])
  gallery['navigation']['firstPage'].click(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['navigation']['lastPage'].click(makeGoToLastPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['navigation']['pageIndex'].change(makeGoToPageAtIndex(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['sort']['by'].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['sort']['order'].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])

  gallery['hidden']['refreshButton'].click(withRefreshFiles(makeGoToPageAtIndex(changePageConfig)), **inputsAndOutputs['hiddenRefreshButton'])
  gallery['hidden']['refreshCounter'].change(withRefreshFiles(makeRefreshPageForCounter(changePageConfig)), **inputsAndOutputs['hiddenRefreshCounter'])

  for (row, buttonRow) in enumerate(gallery['buttons']):
    for (column, button) in enumerate(buttonRow):
      button.click(makeOnImageClick(tabConfig, column, row), **inputsAndOutputs['imageButton'])
  gallery['hidden']['selectedImage'].change(onImageChange, **inputsAndOutputs['selectedImage'])

  for (otherTab, moveToOtherTabButton) in sidePanel['buttons']['moveTo']:
    moveToOtherTabButton.click(makeMoveImage(otherTab), **inputsAndOutputs['moveToTabButton'])
  sidePanel['buttons']['deselect'].click(deselectImage, **inputsAndOutputs['deselectButton'])
