import gradio
from math import ceil

from src.py.config import TabConfig
from src.py.utils.tabs import getTabElementId
from src.py.files import makeDirIfMissing, getImagesInDir

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel

from src.py.images import makeGetImages, getImagesPerPage, imagesIntoData
from src.py.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageWithAtIndex, PageChangingFNConfig


def buttonClickHandler(x: int, y: int):
  print(x, y)

def createTab(tabConfig: TabConfig):
  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig['tabDefaults']
  runtimeConfig = tabConfig["runtimeConfig"]

  makeDirIfMissing(tabConfig['path'])

  allImagesInDir = getImagesInDir(staticConfig, tabConfig['path'] )
  getImages = makeGetImages(tabConfig, allImagesInDir)
  imagesPerPage = getImagesPerPage(tabConfig)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig['suffixes']['galleryTab'], tabConfig)):
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery(
            tabConfig,
            lambda index: imagesIntoData(getImages(index, defaults['sortOrder'], defaults['sortBy'])) if index >= 0 else '',
            buttonClickHandler
          )
          sidePanel = createSidePanel(tabConfig)

  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'pageOffsets': list(range(0 - runtimeConfig['preloadPages'], runtimeConfig['preloadPages'] + 1)),
    'imagesPerPage': imagesPerPage,
    "totalPages": ceil(len(allImagesInDir) / imagesPerPage),
  }

  galleryNavigationInputs = [gallery['pageIndex'], sidePanel['sortOrder'], sidePanel['sortBy']]
  galleryNavigationOutputs = [gallery['pageIndex'], sidePanel['sortOrder'], sidePanel['sortBy'], *gallery['hiddenImagesSrcContainers']]

  gallery['nextPage'].click(makeChangePage(changePageConfig, 1), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['prevPage'].click(makeChangePage(changePageConfig, -1), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['firstPage'].click(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['lastPage'].click(makeGoToLastPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['pageIndex'].change(makeGoToPageWithAtIndex(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  sidePanel['sortBy'].change(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  sidePanel['sortOrder'].change(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
