from os import DirEntry
from typing import TypedDict

from src.py.config import TabConfig

class MissingThumbnail(TypedDict):
  forImage: DirEntry[str]
  forTab: TabConfig

class GetImagesWithMissingThumbnailsOutput(TypedDict):
  output: list[MissingThumbnail]

MUTABLE_getImagesWithMissisngThumbnailsOutputs = dict[str, GetImagesWithMissingThumbnailsOutput]
