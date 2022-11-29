from src.py.config import TabConfig

from modules.script_callbacks import ImageSaveParams

from src.py.modules.shared.files import imageBelongsToTab, getFilenameFromPath
from src.py.modules.thumbnails.logic.generate import generateThumbnail

def makeImageSavedListener(tabConfig: TabConfig):
  def imageSavedListener(image: ImageSaveParams):
    if (imageBelongsToTab(tabConfig, image.filename)):
      generateThumbnail(tabConfig, image.image, getFilenameFromPath(image.filename))
  return imageSavedListener
