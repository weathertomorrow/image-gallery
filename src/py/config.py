from typing import TypedDict, TypeVar, Union, List

from modules.paths import script_path
from modules.shared import opts

ConfigFieldDefaultValue = TypeVar('ConfigFieldDefaultValue')
ConfigField = tuple[ConfigFieldDefaultValue, str]

class RuntimeConfig(TypedDict):
  page_columns: int
  page_rows: int
  root: str
  tabs: str
  max_tabs_sizes: str

class ConfigurableConfig(TypedDict):
  page_columns: ConfigField[int]
  page_rows: ConfigField[int]
  root: ConfigField[str]
  tabs: ConfigField[str]
  max_tabs_sizes: ConfigField[str]

defaultConfigurableConfig: ConfigurableConfig = {
  "page_columns": (6, "Columns per gallery page"),
  "page_rows": (6, "Rows per gallery page"),
  "root": ("outputs", "Root gallery directory (directories for custom tabs will be created in it)"),
  "tabs": ("trash", "Custom tabs in the gallery"),
  "max_tabs_sizes": ("trash:20", "Max amount of images to store in a tab (if not specified, then no limit)")
}

class IdSuffixesConfigs(TypedDict):
  allTabs: str
  tab: str
  tab_row: str
  gallery: str

class StaticConfig(TypedDict):
  extension_id: str
  suffixes: IdSuffixesConfigs
  imageExtensions: List[str]
  builtinTabs: dict[str, str]
  script_path: str

staticConfig: StaticConfig = {
  "extension_id": "images_gallery",
  "script_path": script_path,
  "suffixes": {
    "allTabs": "tabs",
    "tab": "tab",
    "tab_row": "tab_row",
    "gallery": "gallery",
  },
  "imageExtensions": [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"],
  "builtinTabs": {
    "txt2img": opts.outdir_txt2img_samples,
    "img2img": opts.outdir_img2img_samples,
    "Extras": opts.outdir_extras_samples,
    "Favorites": opts.outdir_save
  }
}

class BaseTabConfig(TypedDict):
  displayName: str
  id: str
  maxSize: Union[int, None]
  path: str

class TabConfig(BaseTabConfig):
  runtimeConfig: RuntimeConfig
  staticConfig: StaticConfig


class UILabelsConfig(TypedDict):
  extension_name: str

uiLabelsConfig: UILabelsConfig = {
  "extension_name": "Images gallery"
}
