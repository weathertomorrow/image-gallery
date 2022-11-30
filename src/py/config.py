from typing import TypedDict, TypeVar, Union, List
from enum import Enum

from modules.paths import script_path
from modules.shared import opts

class SortOrder(Enum):
  DESC = 'desc'
  ASC = 'asc'

class SortBy(Enum):
  DATE = 'date'
  FILENAME = 'filename'

ConfigFieldDefaultValue = TypeVar('ConfigFieldDefaultValue')
ConfigField = tuple[ConfigFieldDefaultValue, str]

class RuntimeConfig(TypedDict):
  pageColumns: int
  pageRows: int
  root: str
  tabs: str
  maxTabsSizes: str
  preloadPages: int
  useThumbnails: bool
  modifyTimes: bool

class ConfigurableConfig(TypedDict):
  pageColumns: ConfigField[int]
  pageRows: ConfigField[int]
  root: ConfigField[str]
  tabs: ConfigField[str]
  maxTabsSizes: ConfigField[str]
  preloadPages: ConfigField[int]
  useThumbnails: ConfigField[bool]
  modifyTimes: ConfigField[bool]

defaultConfigurableConfig: ConfigurableConfig = {
  "root": ("outputs", "Root gallery directory (directories for custom tabs will be created in it)"),
  "useThumbnails": (True, "Create & display thumbnails for generated images (speeds up the gallery)"),
  "modifyTimes": (True, "Update image's modification time when moving it"),
  "pageColumns": (6, "Columns per gallery page"),
  "pageRows": (6, "Rows per gallery page"),
  "preloadPages": (2, "Amount of pages to preload in both directions"),
  "tabs": ("trash", "Custom tabs in the gallery"),
  "maxTabsSizes": ("trash:20", "Max amount of images to store in a tab (if not specified, then no limit)"),
}

class IdSuffixesConfigs(TypedDict):
  extensionTab: str
  galleryTab: str
  gallery: str
  galleryContainer: str
  imgSrcs: str
  imgButton: str
  selectedImagePath: str
  moveToButton: str
  refreshButton: str
  hiddenPageIndex: str
  sidePanelButtonsContainer: str
  generateThumbnailsButton: str
  generateThumbnailsContainer: str
  navigationControllsContainer: str

class TabDefaults(TypedDict):
  pageIndex: int
  sortBy: SortBy
  sortOrder: SortOrder

class Thumbnails(TypedDict):
  folderSuffix: str
  filePrefix: str
  maxSize: int

class BuiltinTab(TypedDict):
  path: str
  moveToEnabled: bool
  sendToEnabled: bool

class StaticConfig(TypedDict):
  extensionId: str
  elementsSuffixes: IdSuffixesConfigs
  imageExtensions: List[str]
  builtinTabs: dict[str, BuiltinTab]
  scriptPath: str
  cssClassPrefix: str
  tabDefaults: TabDefaults
  thumbnails: Thumbnails

staticConfig: StaticConfig = {
  "extensionId": "images_gallery",
  "scriptPath": script_path,
  "cssClassPrefix": "image_gallery",
  "thumbnails": {
    "folderSuffix": "-gallery-thumbnails",
    "filePrefix": "thumbnail__",
    "maxSize": 300,
  },
  "elementsSuffixes": {
    "extensionTab": "extensionTab",
    "galleryTab": "galleryTab",
    "gallery": "gallery",
    "galleryContainer": "galleryContainer",
    "navigationControllsContainer": "navigationControllsContainer",
    "imgSrcs": "imgSrcs",
    "imgButton": "imgButton",
    "moveToButton": "moveToButton",
    "refreshButton": "refreshButton",
    "generateThumbnailsButton": "generateThumbnailsButton",
    "generateThumbnailsContainer": "generateThumbnailsContainer",
    "sidePanelButtonsContainer": "sidePanelButtonsContainer",
    "selectedImagePath": "selectedImagePath",
    "hiddenPageIndex": "hiddenPageIndex"
  },
  "tabDefaults": {
    "pageIndex": 0,
    "sortBy": SortBy.DATE,
    "sortOrder": SortOrder.DESC
  },
  "imageExtensions": [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"],
  "builtinTabs": {
    "txt2img": {
      "path": opts.outdir_txt2img_samples,
      "moveToEnabled": False,
      "sendToEnabled": True,
    },
    "img2img": {
      "path":opts.outdir_img2img_samples ,
      "moveToEnabled": False,
      "sendToEnabled": True,
    },
    "Extras": {
      "path": opts.outdir_extras_samples,
      "moveToEnabled": True,
      "sendToEnabled": False,
    },
    "Favorites": {
      "path": opts.outdir_save,
      "moveToEnabled": True,
      "sendToEnabled": False,
    }
  }
}

class GlobalConfig(TypedDict):
  runtimeConfig: RuntimeConfig
  staticConfig: StaticConfig

class BaseTabConfig(BuiltinTab):
  displayName: str
  id: str
  maxSize: Union[int, None]
  path: str
  thumbnailsPath: str

class SingleTabConfig(BaseTabConfig, GlobalConfig):
  pass

class TabConfig(SingleTabConfig):
  otherTabs: list[SingleTabConfig]

class UILabelsConfig(TypedDict):
  extension_name: str

uiLabelsConfig: UILabelsConfig = {
  "extension_name": "Images gallery"
}
