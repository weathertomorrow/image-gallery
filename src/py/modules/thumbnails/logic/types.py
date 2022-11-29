from typing import TypedDict

from src.py.modules.shared.files import ImagesInDir

class GetImagesWithMissingThumbnailsOutput(TypedDict):
  output: ImagesInDir

MUTABLE_getImagesWithMisisngThumbnailsOutputs = dict[str, GetImagesWithMissingThumbnailsOutput]
