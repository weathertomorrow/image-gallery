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

class ConfigurableConfig(TypedDict):
  pageColumns: ConfigField[int]
  pageRows: ConfigField[int]
  root: ConfigField[str]
  tabs: ConfigField[str]
  maxTabsSizes: ConfigField[str]
  preloadPages: ConfigField[int]

defaultConfigurableConfig: ConfigurableConfig = {
  "root": ("outputs", "Root gallery directory (directories for custom tabs will be created in it)"),
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
  imgSrcs: str
  imgButton: str
  moveToButton: str
  hiddenRefreshButton: str

class TabDefaults(TypedDict):
  pageIndex: int
  sortBy: SortBy
  sortOrder: SortOrder

class StaticConfig(TypedDict):
  extensionId: str
  suffixes: IdSuffixesConfigs
  imageExtensions: List[str]
  builtinTabs: dict[str, str]
  scriptPath: str
  cssClassPrefix: str
  tabDefaults: TabDefaults

staticConfig: StaticConfig = {
  "extensionId": "images_gallery",
  "scriptPath": script_path,
  "cssClassPrefix": "image_gallery",
  "suffixes": {
    "extensionTab": "extensionTab",
    "galleryTab": "galleryTab",
    "gallery": "gallery",
    "imgSrcs": "imgSrcs",
    "imgButton": "imgButton",
    "moveToButton": "moveToButton",
    "hiddenRefreshButton": "hiddenRefreshButton",
  },
  "tabDefaults": {
    "pageIndex": 0,
    "sortBy": SortBy.DATE,
    "sortOrder": SortOrder.DESC
  },
  "imageExtensions": [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"],
  "builtinTabs": {
    "txt2img": opts.outdir_txt2img_samples,
    "img2img": opts.outdir_img2img_samples,
    "Extras": opts.outdir_extras_samples,
    "Favorites": opts.outdir_save
  }
}

class GlobalConfig(TypedDict):
  runtimeConfig: RuntimeConfig
  staticConfig: StaticConfig

class BaseTabConfig(TypedDict):
  displayName: str
  id: str
  maxSize: Union[int, None]
  path: str

class SingleTabConfig(BaseTabConfig, GlobalConfig):
  pass

class TabConfig(SingleTabConfig):
  otherTabs: list[SingleTabConfig]

class UILabelsConfig(TypedDict):
  extension_name: str

uiLabelsConfig: UILabelsConfig = {
  "extension_name": "Images gallery"
}
