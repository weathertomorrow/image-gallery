import gradio

from src.py.config import TabConfig
from src.py.utils.str import withSuffix
from src.py.files import makeDirIfMissing

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel

from src.py.images import makeGetImages, getImagesPerPage
from src.py.pages import makeChangePage, mageGoToLastPage, makeGoToFirstPage


def createTab(tabConfig: TabConfig):
  makeDirIfMissing(tabConfig['path'])

  staticConfig = tabConfig["staticConfig"]
  runtimeConfig = tabConfig["runtimeConfig"]

  imagesPerPage = getImagesPerPage(tabConfig)
  getImages = makeGetImages(tabConfig, imagesPerPage)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = withSuffix(staticConfig['suffixes']['tab'], tabConfig["id"])):
    with gradio.Row(elem_id = withSuffix(staticConfig['suffixes']['tab_row'], tabConfig['id'])):
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery(getImages(0))
          sidePanel = createSidePanel()

  gallery["gallery"].value
  gallery['nextPage'].click(makeChangePage(getImages, imagesPerPage, 1), [gallery['pageIndex']], [gallery["gallery"], gallery['pageIndex']])
  gallery['prevPage'].click(makeChangePage(getImages, imagesPerPage, -1), [gallery['pageIndex']], [gallery["gallery"], gallery['pageIndex']])
  gallery['firstPage'].click(makeGoToFirstPage(getImages), [gallery['pageIndex']], [gallery["gallery"], gallery['pageIndex']])
  gallery['lastPage'].click(mageGoToLastPage(getImages), [gallery['pageIndex']], [gallery["gallery"], gallery['pageIndex']])
  gallery['pageIndex'].change(mageGoToLastPage(getImages), [gallery['pageIndex']], [gallery["gallery"], gallery['pageIndex']])
