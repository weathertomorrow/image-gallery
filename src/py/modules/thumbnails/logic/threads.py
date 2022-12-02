from PIL import Image
from os import path, DirEntry
from functools import reduce

from src.py.config import TabConfig
from src.py.modules.shared.files import makeDirIfMissing
from src.py.modules.shared.mutable import getImagesInDirRef
from src.py.modules.shared.list import chunk

from src.py.modules.thumbnails.logic.checks import makeIsMissingThumbnail
from src.py.modules.thumbnails.logic.types import MUTABLE_getImagesWithMissisngThumbnailsOutputs, GetImagesWithMissingThumbnailsOutput, MissingThumbnail
from src.py.modules.shared.names import getThumbnailNameFromImageName

def aggregateMissingThumbnails(aggregator: list[MissingThumbnail], entries: GetImagesWithMissingThumbnailsOutput) -> list[MissingThumbnail]:
  return aggregator + entries["output"]

SplitOutputsChunks = list[list[MissingThumbnail]]
def splitThreadOutputsEvenly(outputs: MUTABLE_getImagesWithMissisngThumbnailsOutputs, threadAmount: int) -> SplitOutputsChunks:
  missingThumbnailsChunks = chunk(reduce(aggregateMissingThumbnails, outputs.values(), []), threadAmount)

  return [ missingThumbnailsChunks[index] for index in range(0, threadAmount) ]

def makeWithTabConfig(tabConfig: TabConfig):
  def withTabConfig(entry: DirEntry[str]) -> MissingThumbnail:
    return {
      "forImage": entry,
      "forTab": tabConfig
    }

  return withTabConfig

def THREAD_getImagesWithMissingThumbnails(tabConfig: TabConfig, outputs: MUTABLE_getImagesWithMissisngThumbnailsOutputs) -> None:
  makeDirIfMissing(tabConfig["path"])
  makeDirIfMissing(tabConfig['thumbnailsPath'])

  allImagesInDir = getImagesInDirRef(tabConfig, tabConfig["path"])
  allThumbnailsInDirDict = { image.name: None for image in getImagesInDirRef(tabConfig, tabConfig["thumbnailsPath"])["images"] }

  outputs[tabConfig["id"]]["output"] = list(map(makeWithTabConfig(tabConfig), filter(makeIsMissingThumbnail(tabConfig, allThumbnailsInDirDict), allImagesInDir["images"])))

def THREAD_generateThumbnails(missingThumbnails: list[MissingThumbnail]) -> None:
  for missingThumbnail in missingThumbnails:
    tabConfig = missingThumbnail["forTab"]
    thumbnailSize = tabConfig["staticConfig"]["thumbnails"]["maxSize"]

    image = Image.open(missingThumbnail["forImage"].path)
    image.thumbnail((thumbnailSize, thumbnailSize))
    image.save(path.join(tabConfig["thumbnailsPath"], getThumbnailNameFromImageName(tabConfig, missingThumbnail["forImage"].name)))
