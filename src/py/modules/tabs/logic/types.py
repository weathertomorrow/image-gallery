from typing import TypedDict, Callable, Union

from src.py.config import SortBy, SortOrder
from src.py.modules.shared.mutable import MUTABLE_ImagesInDirRef

# importing types in python can cause dependecy cycles

class ImageOnPage(TypedDict):
  imagePath: str
  thumbnailPath: Union[str, None]

ImagesPage = list[ImageOnPage]
GetImages = Callable[[float, SortOrder, SortBy], ImagesPage]

PostProcess = Callable[[ImagesPage], str]

PageChangingFNOutput = tuple[
  int, # current page index
  str, # sort order
  str, # sort by,
  str, # each page of images' sources after postprocessing
]

PageChangingFN = Callable[[str, str, int], PageChangingFNOutput]

class PageChangingFNConfig(TypedDict):
  getImages: GetImages
  imagesInDirRef: MUTABLE_ImagesInDirRef
  postProcess: PostProcess
  pageOffsets: list[int]
  imagesPerPage: int
