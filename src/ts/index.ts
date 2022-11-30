import config from './config'
import { initTab } from './tab'
import { isNotNil } from './utils/guards'
import { includeOtherTabConfigs, makeExpandConfig } from './utils/config'
import { tabElementQueryString } from './utils/str'

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const preloadRoot = document.createElement('div')
    document.body.appendChild(preloadRoot)

    const root = document.body
      .querySelector(config.gradioAppTag)
      ?.shadowRoot

    Array.from(root
      ?.querySelector(tabElementQueryString(config, 'extensionTab'))
      ?.querySelectorAll<HTMLElement>(tabElementQueryString(config, 'galleryTab')) ?? []
    )
      .map(makeExpandConfig(config, preloadRoot, root))
      .filter(isNotNil)
      .map(includeOtherTabConfigs)
      .forEach(initTab)
  }, 1000)
})
