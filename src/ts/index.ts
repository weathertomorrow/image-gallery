import staticConfig from './config'
import { initTab } from './tab'
import { isNotNil } from './utils/guards'
import { includeOtherTabConfigs, makeExpandConfig } from './utils/config'
import { tabElementQueryString } from './utils/str'
import { createEmptyContainer } from './utils/elements'

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const preloadRoot = createEmptyContainer(document.body)

    const appRoot = document.body
      .querySelector(staticConfig.gradio.appTag)
      ?.shadowRoot

    Array.from(appRoot
      ?.querySelector(tabElementQueryString(staticConfig, 'extensionTab'))
      ?.querySelectorAll<HTMLElement>(tabElementQueryString(staticConfig, 'galleryTab')) ?? []
    )
      .map(makeExpandConfig({ staticConfig, appRoot, preloadRoot }))
      .filter(isNotNil)
      .map(includeOtherTabConfigs)
      .forEach(initTab)
  }, 1000)
})
