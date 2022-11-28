import gradio
from os import stat, path
from shutil import move
from modules.script_callbacks import ImageSaveParams

from typing import Callable, Union, TypedDict, List, cast
from time import strftime, localtime

from modules.extras import run_pnginfo

from src.py.ui.gallery import Gallery
from src.py.ui.sidePanel import SidePanel
from src.py.config import TabConfig, SingleTabConfig
from src.py.images import dataIntoImags

OnNewImage = Callable[[ImageSaveParams], None]
ImageCreationListener = Callable[[ImageSaveParams], None]

def makeImageCreationListener(tabConfig: TabConfig, onNewImage: OnNewImage) -> ImageCreationListener:
  def imageCreationListener(image: ImageSaveParams):
    commonPath = path.commonpath([tabConfig['path'], image.filename])
    print(tabConfig['id'], commonPath)

    if not commonPath:
      return

    if path.samefile(commonPath, tabConfig['path']):
        onNewImage(image)

  return imageCreationListener

def makeOnNewImage(gallery: Gallery) -> OnNewImage:
  def onNewImage(image: ImageSaveParams):
    gallery['navigation']['pageIndex'].

  return onNewImage

def formatImageTime(time: float) -> str:
  return "<div style='color:#999' align='right'>" + strftime("%Y-%m-%d %H:%M:%S", localtime(time)) + "</div>"

ButtonClickHandler = Callable[[str], tuple]
def makeOnImageClick(tabConfig: TabConfig, x: int, y: int) -> ButtonClickHandler:
  def onImageClick(imagesInHtml: str):
    image = dataIntoImags(imagesInHtml)[y * tabConfig['runtimeConfig']['pageColumns'] + x]
    return (image, image, formatImageTime(stat(image).st_ctime))

  return onImageClick

def onImageChange(image: Union[gradio.Pil, None]):
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


AllGradioInputs = Union[gradio.Textbox, gradio.HTML, gradio.Number, gradio.Image, gradio.Radio]
AllGradioOutputs = Union[gradio.Textbox, gradio.HTML, gradio.Number, gradio.Image, gradio.Radio, gradio.Column]

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

class UNSAFE_UntypedInputOutputPairs(TypedDict):
  navigation: UNSAFE_InputOutputPair
  imageButton: UNSAFE_InputOutputPair
  deselectButton: UNSAFE_InputOutputPair
  selectedImage: UNSAFE_InputOutputPair
  moveToTabButton: UNSAFE_InputOutputPair

# untyped because idk how to get the base "Component" type that gradio wants (doesnt seem to be exposed by gradio)
def getEventInputsAndOutputs(gallery: Gallery, sidePanel: SidePanel) -> UNSAFE_UntypedInputOutputPairs:
  navigation: InputOutputPair = {
    "inputs": [gallery['navigation']['pageIndex'], gallery['sort']['order'], gallery['sort']['by']],
    "outputs": [gallery['navigation']['pageIndex'], gallery['sort']['order'], gallery['sort']['by'], *gallery['hiddenImagesSrcContainers']]
  }

  selectedImage: InputOutputPair = {
    "inputs": [gallery['hiddenSelectedImage']],
    "outputs": [sidePanel['image']['prompts'], sidePanel['container']]
  }

  deselectButton: InputOutputPair = {
    "inputs": None,
    "outputs": [gallery['hiddenSelectedImage']]
  }

  imageButton: InputOutputPair = {
    "inputs": [gallery['hiddenImagesSrcContainers'][len(gallery['hiddenImagesSrcContainers']) // 2]],
    "outputs":[gallery['hiddenSelectedImage'], sidePanel['image']['name'], sidePanel['image']['creationTime']]
  }

  moveToTab: InputOutputPair = {
    "inputs": [sidePanel['image']['name']],
    "outputs": None
  }

  returnValue: InputOutputPairs = {
    "navigation": navigation,
    "selectedImage": selectedImage,
    "deselectButton": deselectButton,
    "imageButton": imageButton,
    "moveToTabButton": moveToTab,
  }

  return cast(UNSAFE_UntypedInputOutputPairs, returnValue)
