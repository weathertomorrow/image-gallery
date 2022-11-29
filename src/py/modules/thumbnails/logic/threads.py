from PIL import Image
from os import path, DirEntry
from functools import reduce

from src.py.config import TabConfig
from src.py.modules.shared.files import makeDirIfMissing
from src.py.modules.shared.mutable import getImagesInDirRef
from src.py.modules.shared.list import chunk

from src.py.modules.thumbnails.logic.checks import makeIsMissingThumbnail
from src.py.modules.thumbnails.logic.types import MUTABLE_getImagesWithMisisngThumbnailsOutputs, GetImagesWithMissingThumbnailsOutput
from src.py.modules.shared.names import getThumbnailNameFromImageName

def aggregateMissingThumbnails(aggregator: list[DirEntry[str]], entries: GetImagesWithMissingThumbnailsOutput) -> list[DirEntry[str]]:
  return aggregator + entries["output"]

def splitThreadOutputsEvenly(outputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs) -> MUTABLE_getImagesWithMisisngThumbnailsOutputs:
  tabIds = outputs.keys()
  missingThumbnailsChunks = chunk(reduce(aggregateMissingThumbnails, outputs.values(), []), len(tabIds))

  return { tabId: { "output": missingThumbnailsChunks[index] } for (index, tabId) in enumerate(tabIds) }


def THREAD_getImagesWithMissingThumbnails(tabConfig: TabConfig, outputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs) -> None:
  makeDirIfMissing(tabConfig["path"])
  makeDirIfMissing(tabConfig['thumbnailsPath'])

  allImagesInDir = getImagesInDirRef(tabConfig, tabConfig["path"])
  allThumbnailsInDirDict = { image.name: None for image in getImagesInDirRef(tabConfig, tabConfig["thumbnailsPath"])["images"] }

  output = outputs[tabConfig["id"]]
  output["output"] = list(filter(makeIsMissingThumbnail(tabConfig, allThumbnailsInDirDict), allImagesInDir["images"]))


def THREAD_generateThumbnails(tabConfig: TabConfig, missingThumbnails: GetImagesWithMissingThumbnailsOutput) -> None:
  thumbnailSize = tabConfig["staticConfig"]["thumbnails"]["maxSize"]

  for missingThumbnail in missingThumbnails["output"]:
    image = Image.open(missingThumbnail.path)
    image.thumbnail((thumbnailSize, thumbnailSize))
    image.save(path.join(tabConfig["thumbnailsPath"], getThumbnailNameFromImageName(tabConfig, missingThumbnail.name)))
