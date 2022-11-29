import gradio
from threading import Thread
from typing import cast

from src.py.config import TabConfig
from src.py.modules.shared.str import getExtensionElementId

from src.py.modules.thumbnails.logic.threads import  THREAD_generateThumbnails, THREAD_getImagesWithMissingThumbnails, splitThreadOutputsEvenly
from src.py.modules.thumbnails.logic.checks import isMissingThumbnails
from src.py.modules.thumbnails.logic.types import MUTABLE_getImagesWithMisisngThumbnailsOutputs

htmlInfoMessage = {
  "missingThumbnails": '<p style="text-align: center; color: red">Some thumbnails are missing</p>',
  "generatingThumbnails": '<p style="text-align: center;">Thumbnails are being generated (make take a while)…</br>You can use the gallery normally</p>'
}

def makeGenerateThumbnails(tabConfigs: list[TabConfig], outputsFromTabs: MUTABLE_getImagesWithMisisngThumbnailsOutputs):
  def generateThumbnails(_: float):
    threads: list[Thread]  = []
    threadOutputs = splitThreadOutputsEvenly(outputsFromTabs)

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

def onButtonClick():
  return (1, htmlInfoMessage["generatingThumbnails"], gradio.Button.update(visible = False))

def hadleMissingThumbnails(tabsConfigs: list[TabConfig]):
  staticConfig = tabsConfigs[0]["staticConfig"]

  threadOutputs: MUTABLE_getImagesWithMisisngThumbnailsOutputs = {
    tabConfig["id"]: { "output": []}  for tabConfig in tabsConfigs
  }

  threads = [Thread(target = THREAD_getImagesWithMissingThumbnails, args = (tabConfig, threadOutputs)) for tabConfig in tabsConfigs]

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()

  if (any([isMissingThumbnails(output) for output in threadOutputs.values()])):
    with gradio.Row(elem_id = getExtensionElementId(staticConfig["elementsSuffixes"]["generateThumbnailsContainer"], staticConfig)) as container:
      with gradio.Column():
        messageContainer = gradio.HTML(value = htmlInfoMessage["missingThumbnails"])

        # change of this actually generates thumbnails, clicking a button triggers the change and shows loading
        hiddenCounter = gradio.Number(value = 0, visible = False)
        # not sure why gradio doesnt want the row as output, it works fine
        hiddenCounter.change(makeGenerateThumbnails(tabsConfigs, threadOutputs), [hiddenCounter], cast(None, container))

        button = gradio.Button(value = 'Generate missing thumbnails (may take a while)', elem_id = getExtensionElementId(staticConfig["elementsSuffixes"]["generateThumbnailsButton"], staticConfig))
        button.click(onButtonClick, None, [hiddenCounter, messageContainer, button])
