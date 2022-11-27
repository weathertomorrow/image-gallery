import gradio

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
  runtimeConfig = tabConfig["runtimeConfig"]

  imagesPerPage = getImagesPerPage(tabConfig)
  getImages = makeGetImages(tabConfig, imagesPerPage)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig['suffixes']['galleryTab'], tabConfig)):
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery(tabConfig, imagesIntoData(getImages(0)), buttonClickHandler)
          sidePanel = createSidePanel(tabConfig)

  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'imagesPerPage': imagesPerPage
  }

  gallery['nextPage'].click(makeChangePage(changePageConfig, 1), [gallery['pageIndex']], [gallery['hiddenImagesSrcContainer'], gallery['pageIndex']])
  gallery['prevPage'].click(makeChangePage(changePageConfig, -1), [gallery['pageIndex']], [gallery['hiddenImagesSrcContainer'], gallery['pageIndex']])
  gallery['firstPage'].click(makeGoToFirstPage(changePageConfig), [gallery['pageIndex']], [gallery['hiddenImagesSrcContainer'], gallery['pageIndex']])
  gallery['lastPage'].click(makeGoToLastPage(changePageConfig), [gallery['pageIndex']], [gallery['hiddenImagesSrcContainer'], gallery['pageIndex']])
  gallery['pageIndex'].change(makeGoToPageWithAtIndex(changePageConfig), [gallery['pageIndex']], [gallery['hiddenImagesSrcContainer'], gallery['pageIndex']])
