import gradio
from os import stat
from typing import Callable, Union, TypedDict, List, cast
from time import strftime, localtime

from modules.extras import run_pnginfo

from src.py.config import TabConfig, SingleTabConfig
from src.py.modules.shared.mutable import MUTABLE_ImagesInDirRef
from src.py.modules.shared.files import getFilenameFromPath, moveFileAndPreventDuplicates

from src.py.modules.tabs.ui.gallery import Gallery
from src.py.modules.tabs.ui.sidePanel import SidePanel
from src.py.modules.tabs.logic.images import dataIntoImages

def formatImageTime(time: float) -> str:
  return "<div style='color:#999' align='right'>" + strftime("%Y-%m-%d %H:%M:%S", localtime(time)) + "</div>"

ButtonClickHandler = Callable[[str], tuple]
def makeOnImageClick(tabConfig: TabConfig, x: int, y: int) -> ButtonClickHandler:
  def onImageClick(imagesInHtml: str):
    image = dataIntoImages(imagesInHtml)[y * tabConfig["runtimeConfig"]["pageColumns"] + x]["imagePath"]
    return (image, image, formatImageTime(stat(image).st_ctime))

  return onImageClick

def onImageChange(image: Union[gradio.Pil, None]):
  if image is None:
    return ("", gradio.update(visible = False))

  imageInfo = run_pnginfo(image)
  return (imageInfo[1], gradio.update(visible = True))

def deselectImage():
  return None

def makeMoveImage(targetTab: SingleTabConfig, imagesInDir: MUTABLE_ImagesInDirRef):
  # these are here because files need to be refreshed afterwards
  def moveImage(sortOrder: str, sortBy: str, image: str, counter: float):
    moveFileAndPreventDuplicates(image, targetTab["path"], targetTab["runtimeConfig"]["modifyTimes"])

    imageName = getFilenameFromPath(image)
    imageThumbnail = (
        imagesInDir["thumbnails"][imageName]
      if
        targetTab["runtimeConfig"]["useThumbnails"] and imageName in imagesInDir["thumbnails"]
      else
        None
    )

    if imageThumbnail is not None:
        moveFileAndPreventDuplicates(imageThumbnail, targetTab["thumbnailsPath"])

    return (None, 0 if int(counter) == 1 else 1)

  return moveImage

AllGradioInputs = Union[gradio.Textbox, gradio.HTML, gradio.Number, gradio.Image, gradio.Radio, gradio.Button]
AllGradioOutputs = Union[gradio.Textbox, gradio.HTML, gradio.Number, gradio.Image, gradio.Radio, gradio.Column, gradio.Button]

class InputOutputPair(TypedDict):
  inputs: Union[None, List[AllGradioInputs]]
  outputs: Union[None, List[AllGradioOutputs]]

class UNSAFE_InputOutputPair(TypedDict):
  inputs: None
  outputs: None

class InputOutputPairs(TypedDict):
  navigation: InputOutputPair
  imageButton: InputOutputPair
  deselectButton: InputOutputPair
  selectedImage: InputOutputPair
  moveToTabButton: InputOutputPair
  hiddenRefreshButton: InputOutputPair
  hiddenRefreshCounter: InputOutputPair

class UNSAFE_UntypedInputOutputPairs(TypedDict):
  navigation: UNSAFE_InputOutputPair
  imageButton: UNSAFE_InputOutputPair
  deselectButton: UNSAFE_InputOutputPair
  selectedImage: UNSAFE_InputOutputPair
  moveToTabButton: UNSAFE_InputOutputPair
  hiddenRefreshButton: UNSAFE_InputOutputPair
  hiddenRefreshCounter: UNSAFE_InputOutputPair

# untyped because not sure how to get the base "Component" type that gradio wants (doesnt seem to be exposed by gradio)
def getEventInputsAndOutputs(gallery: Gallery, sidePanel: SidePanel) -> UNSAFE_UntypedInputOutputPairs:
  sortArgOrder = (gallery["sort"]["order"], gallery["sort"]["by"])

  navigation: InputOutputPair = {
    "inputs": [*sortArgOrder, gallery["navigation"]["pageIndex"]],
    "outputs": [gallery["navigation"]["pageIndex"], *sortArgOrder, *gallery["hidden"]["imagesSrcContainers"]]
  }

  hiddenRefreshButton: InputOutputPair = {
    "inputs": [*sortArgOrder, gallery["navigation"]["pageIndex"]],
    "outputs": [gallery["navigation"]["pageIndex"], *sortArgOrder, *gallery["hidden"]["imagesSrcContainers"]]
  }

  hiddenRefreshCounter: InputOutputPair = {
    "inputs": [*sortArgOrder, gallery["navigation"]["pageIndex"], gallery["hidden"]["refreshCounter"]],
    "outputs": [gallery["navigation"]["pageIndex"], *sortArgOrder, gallery["hidden"]["refreshCounter"], *gallery["hidden"]["imagesSrcContainers"]]
  }

  moveToTab: InputOutputPair = {
    "inputs": [*sortArgOrder, sidePanel["image"]["name"], gallery["hidden"]["refreshCounter"]],
    "outputs": [gallery["hidden"]["selectedImage"], gallery["hidden"]["refreshCounter"]]
  }

  selectedImage: InputOutputPair = {
    "inputs": [gallery["hidden"]["selectedImage"]],
    "outputs": [sidePanel["image"]["prompts"], sidePanel["container"]]
  }

  deselectButton: InputOutputPair = {
    "inputs": None,
    "outputs": [gallery["hidden"]["selectedImage"]]
  }

  imageButton: InputOutputPair = {
    "inputs": [gallery["hidden"]["imagesSrcContainers"][len(gallery["hidden"]["imagesSrcContainers"]) // 2]],
    "outputs":[gallery["hidden"]["selectedImage"], sidePanel["image"]["name"], sidePanel["image"]["creationTime"]]
  }

  returnValue: InputOutputPairs = {
    "navigation": navigation,
    "selectedImage": selectedImage,
    "deselectButton": deselectButton,
    "imageButton": imageButton,
    "moveToTabButton": moveToTab,
    "hiddenRefreshButton": hiddenRefreshButton,
    "hiddenRefreshCounter": hiddenRefreshCounter
  }

  return cast(UNSAFE_UntypedInputOutputPairs, returnValue)
