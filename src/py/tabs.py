import gradio
from math import ceil
from os import stat, path
from shutil import move

from typing import Callable, Union
from time import strftime, localtime

from modules.extras import run_pnginfo

from src.py.config import TabConfig, SingleTabConfig
from src.py.utils.tabs import getTabElementId
from src.py.files import makeDirIfMissing, getImagesInDir

from src.py.ui.gallery import createGallery
from src.py.ui.sidePanel import createSidePanel

from src.py.images import makeGetImages, getImagesPerPage, imagesIntoData, dataIntoImags
from src.py.pages import makeChangePage, makeGoToLastPage, makeGoToFirstPage, makeGoToPageWithAtIndex, PageChangingFNConfig

def formatImageTime(time: float) -> str:
  return "<div style='color:#999' align='right'>" + strftime("%Y-%m-%d %H:%M:%S", localtime(time)) + "</div>"

ButtonClickHandler = Callable[[str, int, int], tuple]
def makeButtonClickHandler(tabConfig: TabConfig) -> ButtonClickHandler:
  def buttonClickHandler(imagesInHtml: str, x: int, y: int):
    image = dataIntoImags(imagesInHtml)[y * tabConfig['runtimeConfig']['pageColumns'] + x]
    return (image, image, formatImageTime(stat(image).st_ctime))

  return buttonClickHandler

def imageChangeHandler(image: Union[gradio.Pil, None]):
  if image is None:
    return ("", gradio.update(visible = False))

  imageInfo = run_pnginfo(image)
  return (imageInfo[1], gradio.update(visible = True))

def deselectImage():
  return None

def makeMoveImage(targetTab: SingleTabConfig):
  def moveImage(image: str):
    move(image, targetTab['path'])

  return moveImage

def createTab(tabConfig: TabConfig):
  makeDirIfMissing(tabConfig['path'])

  staticConfig = tabConfig["staticConfig"]
  defaults = staticConfig['tabDefaults']
  runtimeConfig = tabConfig["runtimeConfig"]

  allImagesInDir = getImagesInDir(staticConfig, tabConfig['path'])
  getImages = makeGetImages(tabConfig, allImagesInDir)
  imagesPerPage = getImagesPerPage(tabConfig)
  buttonClickHandler = makeButtonClickHandler(tabConfig)

  with gradio.Tab(label = tabConfig["displayName"], elem_id = getTabElementId(staticConfig['suffixes']['galleryTab'], tabConfig)):
    with gradio.Row():
      with gradio.Column():
        with gradio.Row():
          gallery = createGallery({
            "tabConfig": tabConfig,
            "getImagesPage": lambda index: imagesIntoData(getImages(index, defaults['sortOrder'], defaults['sortBy'])) if index >= 0 else '',
          })
          sidePanel = createSidePanel(tabConfig)


  changePageConfig: PageChangingFNConfig = {
    'getImages': getImages,
    'postProcess': imagesIntoData,
    'pageOffsets': list(range(0 - runtimeConfig['preloadPages'], runtimeConfig['preloadPages'] + 1)),
    'imagesPerPage': imagesPerPage,
    "totalPages": ceil(len(allImagesInDir) / imagesPerPage),
  }

  galleryNavigationInputs = [gallery['navigation']['pageIndex'], gallery['sort']['order'], gallery['sort']['by']]
  galleryNavigationOutputs = [gallery['navigation']['pageIndex'], gallery['sort']['order'], gallery['sort']['by'], *gallery['hiddenImagesSrcContainers']]

  imageButtonInputs = [gallery['hiddenImagesSrcContainers'][len(gallery['hiddenImagesSrcContainers']) // 2]]
  imageButtonOutputs = [gallery['hiddenSelectedImage'], sidePanel['image']['name'], sidePanel['image']['creationTime']]

  selectedImageInputs = [gallery['hiddenSelectedImage']]
  selectedImageOutputs = [sidePanel['image']['prompts'], sidePanel['container']]

  gallery['navigation']['nextPage'].click(makeChangePage(changePageConfig, 1), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['navigation']['prevPage'].click(makeChangePage(changePageConfig, -1), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['navigation']['firstPage'].click(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['navigation']['lastPage'].click(makeGoToLastPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['navigation']['pageIndex'].change(makeGoToPageWithAtIndex(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['sort']['by'].change(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)
  gallery['sort']['order'].change(makeGoToFirstPage(changePageConfig), galleryNavigationInputs, galleryNavigationOutputs)

  for (row, buttonRow) in enumerate(gallery['buttons']):
    for (column, button) in enumerate(buttonRow):
      button.click(lambda htmlInput, x = column, y = row: buttonClickHandler(htmlInput, x, y), imageButtonInputs, imageButtonOutputs)
  gallery['hiddenSelectedImage'].change(imageChangeHandler, selectedImageInputs, selectedImageOutputs)


  for (otherTab, moveToOtherTabButton) in sidePanel['buttons']['moveTo']:
    moveToOtherTabButton.click(makeMoveImage(otherTab), [sidePanel['image']['name']], None)

  sidePanel['buttons']['deselect'].click(deselectImage, None, [gallery['hiddenSelectedImage']])
