from PIL import Image
from os import DirEntry, path

from src.py.config import TabConfig

from src.py.modules.shared.names import getThumbnailNameFromImageName

def generateThumbnail(tabConfig: TabConfig, image: Image.Image, imageName: str):
  thumbnailSize = tabConfig["staticConfig"]["thumbnails"]["maxSize"]
  thumbnailName = getThumbnailNameFromImageName(tabConfig, imageName)

  image.thumbnail((thumbnailSize, thumbnailSize))
  image.save(path.join(tabConfig["thumbnailsPath"], thumbnailName))

def generateThumbnailFromPath(tabConfig: TabConfig, forImage: DirEntry[str]):
  image = Image.open(forImage.path)
  generateThumbnail(tabConfig, image, forImage.name)
