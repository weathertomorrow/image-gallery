import gradio
from threading import Thread
from typing import cast

from src.py.config import TabConfig

from src.py.modules.thumbnails.logic.threads import  THREAD_generateThumbnails, THREAD_getImagesWithMissingThumbnails
from src.py.modules.thumbnails.logic.checks import isMissingThumbnails
from src.py.modules.thumbnails.logic.types import MUTABLE_getImagesWithMisisngThumbnailsOutputs

def makeGenerateThumbnails(tabConfigs: list[TabConfig], threadOutputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs):
  def generateThumbnails():
    threads: list[Thread]  = []

    for tabConfig in tabConfigs:
      tabThreadOutput = threadOutputs[tabConfig["id"]]

      if (isMissingThumbnails(tabThreadOutput)):
        thread = Thread(target = THREAD_generateThumbnails, args = (tabConfig, tabThreadOutput))
        threads.append(thread)
        thread.start()

    for thread in threads:
      thread.join()

    return gradio.update(visible = False)
  return generateThumbnails


def hadleMissingThumbnails(tabsConfigs: list[TabConfig]):
  threadOutputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs = {
    tabConfig["id"]: { "output": []}  for tabConfig in tabsConfigs
  }

  threads = [Thread(target = THREAD_getImagesWithMissingThumbnails, args = (tabConfig, threadOutputs)) for tabConfig in tabsConfigs]

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()

  if (any([isMissingThumbnails(output) for output in threadOutputs.values()])):
    with gradio.Row() as container:
      with gradio.Column():
        gradio.HTML(value = '<p style="text-align: center; color: red">Some thumbnails are missing</p>')

        button = gradio.Button(value = 'Generate missing thumbnails (may take a while)')
        # not sure why gradio doesnt want the row as output, it works fine
        button.click(makeGenerateThumbnails(tabsConfigs, threadOutputs), None, cast(None, container))
