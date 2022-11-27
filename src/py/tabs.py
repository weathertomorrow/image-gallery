import gradio
from typing import cast

from src.py.config import TabConfig
from src.py.utils.tabs import getTabElementId
from src.py.files import makeDirIfMissing

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel

from src.py.images import makeGetImages, getImagesPerPage, imagesIntoData
from src.py.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageWithAtIndex, PageChangingFNConfig


def buttonClickHandler(x: int, y: int):
  print(x, y)

def createTab(tabConfig: TabConfig):
  makeDirIfMissing(tabConfig['path'])

  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig['tabDefaults']
  runtimeConfig = tabConfig["runtimeConfig"]


  imagesPerPage = getImagesPerPage(tabConfig)
  getImages = makeGetImages(tabConfig, imagesPerPage)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig['suffixes']['galleryTab'], tabConfig)):
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery(tabConfig, imagesIntoData(getImages(0, defaults['sortOrder'], defaults['sortBy'])), buttonClickHandler)
          sidePanel = createSidePanel(tabConfig)

  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'imagesPerPage': imagesPerPage
  }

  galleryNavigationInputs = [gallery['pageIndex'], sidePanel['sortOrder'], sidePanel['sortBy']]
  galleryNavigationOutputs = [gallery['hiddenImagesSrcContainer'], gallery['pageIndex'], sidePanel['sortOrder'], sidePanel['sortBy']]

  # gradio doesn't expose the "Component" class and for whatever reason, this is not assignable to inputs if not passed directly
  UNSAFE_CAST_galleryNavigationInputs = cast(None, galleryNavigationInputs)

  gallery['nextPage'].click(makeChangePage(changePageConfig, 1), UNSAFE_CAST_galleryNavigationInputs, galleryNavigationOutputs)
  gallery['prevPage'].click(makeChangePage(changePageConfig, -1), UNSAFE_CAST_galleryNavigationInputs, galleryNavigationOutputs)
  gallery['firstPage'].click(makeGoToFirstPage(changePageConfig), UNSAFE_CAST_galleryNavigationInputs, galleryNavigationOutputs)
  gallery['lastPage'].click(makeGoToLastPage(changePageConfig), UNSAFE_CAST_galleryNavigationInputs, galleryNavigationOutputs)
  gallery['pageIndex'].change(makeGoToPageWithAtIndex(changePageConfig), UNSAFE_CAST_galleryNavigationInputs, galleryNavigationOutputs)

  # sidePanel['sortBy'].change(makeGoToPageWithAtIndex(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  # sidePanel['sortOrder'].change(makeGoToPageWithAtIndex(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
