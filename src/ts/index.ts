import { getConfigWithExternalElements, getConfigWithOtherTabs, getConfigWithTabInfo, makeGetConfigWithElements } from './config'
import { staticConfig } from './config/staticConfig'
import { extensionElementById } from './elements/utils'
import { initTab } from './tab'
import { createEmptyContainer } from './utils/dom'
import { flow } from './utils/fn'
import { isNotNil } from './utils/guards'

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const preloadRoot = createEmptyContainer(document.body)

    const appRoot = document.body
      .querySelector(staticConfig.gradio.appTag)
      ?.shadowRoot

    Array.from(appRoot
      ?.querySelector(extensionElementById(staticConfig, 'extensionTab'))
      ?.querySelectorAll<HTMLElement>(extensionElementById(staticConfig, 'galleryTab')) ?? []
    )
      .map(flow(makeGetConfigWithElements({ staticConfig, appRoot, preloadRoot }), getConfigWithTabInfo))
      .map(getConfigWithOtherTabs)
      .map(getConfigWithExternalElements)
      .filter(isNotNil)
      .forEach(initTab)
  }, 1000)
})
