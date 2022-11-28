from os import DirEntry
from typing import Union, TypedDict, Callable

from src.py.config import SortBy, SortOrder

# importing types in python can cause dependecy cycles

ImagesInDir = list[DirEntry[str]]
ImageSortingKey = Callable[[DirEntry[str]],  Union[str, float]]
GetImages = Callable[[float, SortOrder, SortBy], list[str]]
PostProcess = Callable[[list[str]], str]

class MUTABLE_ImagesInDirRef(TypedDict):
  images: ImagesInDir
  prevSortBy: Union[SortBy, None]
  prevSortOrder: Union[SortOrder, None]

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
