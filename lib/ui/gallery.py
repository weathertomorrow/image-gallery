import gradio
from typing import TypedDict, List

class Gallery(TypedDict):
  firstPage: gradio.Button
  prevPage: gradio.Button
  pageIndex: gradio.Number
  nextPage: gradio.Button
  lastPage: gradio.Button
  gallery: gradio.HTML

def createGallery(initialImages: List[str]) -> Gallery:
  with gradio.Column(scale = 2):
    with gradio.Row():
      firstPage = gradio.Button('First Page')
      prevPage = gradio.Button('Prev Page')
      pageIndex = gradio.Number(value = 0, label="Page Index")
      nextPage = gradio.Button('Next Page')
      lastPage = gradio.Button('Last Page')

    gallery = gradio.HTML(value = ','.join(initialImages))

  return {
    "firstPage": firstPage,
    "prevPage": prevPage,
    "pageIndex": pageIndex,
    "nextPage": nextPage,
    "lastPage": lastPage,
    "gallery": gallery,
  }
