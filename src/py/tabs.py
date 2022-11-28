import gradio
from math import ceil


from src.py.config import TabConfig
from src.py.utils.tabs import getTabElementId
from src.py.files import makeDirIfMissing, getImagesInDir

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel

from src.py.images import makeGetImages, getImagesPerPage, imagesIntoData
from src.py.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageWithAtIndex, PageChangingFNConfig
from src.py.eventHandlers import makeButtonClickHandler, imageChangeHandler, makeMoveImage, deselectImage, getEventInputsAndOutputs

def createTab(tabConfig: TabConfig):
  makeDirIfMissing(tabConfig['path'])

  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig['tabDefaults']
  runtimeConfig = tabConfig["runtimeConfig"]

  allImagesInDir = getImagesInDir(staticConfig, tabConfig['path'])
  getImages = makeGetImages(tabConfig, allImagesInDir)
  imagesPerPage = getImagesPerPage(tabConfig)

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
    'pageOffsets': list(range(0 - runtimeConfig['preloadPages'], runtimeConfig['preloadPages'] + 1)),
    'imagesPerPage': imagesPerPage,
    "totalPages": ceil(len(allImagesInDir) / imagesPerPage),
  }

  gallery['navigation']['nextPage'].click(makeChangePage(changePageConfig, 1), **inputsAndOutputs['navigation'])
  gallery['navigation']['prevPage'].click(makeChangePage(changePageConfig, -1), **inputsAndOutputs['navigation'])
  gallery['navigation']['firstPage'].click(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['navigation']['lastPage'].click(makeGoToLastPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['navigation']['pageIndex'].change(makeGoToPageWithAtIndex(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['sort']['by'].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])
  gallery['sort']['order'].change(makeGoToFirstPage(changePageConfig), **inputsAndOutputs['navigation'])

  for (row, buttonRow) in enumerate(gallery['buttons']):
    for (column, button) in enumerate(buttonRow):
      button.click(makeButtonClickHandler(tabConfig, column, row), **inputsAndOutputs['imageButton'])
  gallery['hiddenSelectedImage'].change(imageChangeHandler, **inputsAndOutputs['selectedImage'])

  for (otherTab, moveToOtherTabButton) in sidePanel['buttons']['moveTo']:
    moveToOtherTabButton.click(makeMoveImage(otherTab), **inputsAndOutputs['moveToTabButton'])

  sidePanel['buttons']['deselect'].click(deselectImage, **inputsAndOutputs['deselectButton'])
