from PIL import Image
from os import path

from src.py.config import TabConfig
from src.py.modules.shared.files import makeDirIfMissing
from src.py.modules.shared.mutable import getImagesInDirRef

from src.py.modules.thumbnails.logic.checks import makeIsMissingThumbnail
from src.py.modules.thumbnails.logic.types import MUTABLE_getImagesWithMisisngThumbnailsOutputs, GetImagesWithMissingThumbnailsOutput
from src.py.modules.thumbnails.logic.names import getThumbnailNameFromImageName

def THREAD_getImagesWithMissingThumbnails(tabConfig: TabConfig, outputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs) -> None:
  staticConfig = tabConfig["staticConfig"]
  makeDirIfMissing(tabConfig["path"])
  makeDirIfMissing(tabConfig['thumbnailsPath'])

  allImagesInDir = getImagesInDirRef(tabConfig, staticConfig, tabConfig["path"])
  allThumbnailsInDirDict = { image.name: None for image in getImagesInDirRef(tabConfig, staticConfig, tabConfig["thumbnailsPath"])["images"] }

  output = outputs[tabConfig["id"]]
  output["output"] = list(filter(makeIsMissingThumbnail(tabConfig, allThumbnailsInDirDict), allImagesInDir["images"]))


def THREAD_generateThumbnails(tabConfig: TabConfig, missingThumbnails: GetImagesWithMissingThumbnailsOutput) -> None:
  thumbnailSize = tabConfig["staticConfig"]["thumbnails"]["maxSize"]

  for missingThumbnail in missingThumbnails["output"]:
    image = Image.open(missingThumbnail.path)

    image.thumbnail((thumbnailSize, thumbnailSize))
    image.save(path.join(tabConfig["thumbnailsPath"], getThumbnailNameFromImageName(tabConfig, missingThumbnail.name)))
