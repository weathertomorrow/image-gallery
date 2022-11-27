import config from './config'
import { makeInitTab } from './tab'
import { tabElementQueryString } from './utils/str'

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const root = document.body
      .querySelector(config.gradioAppTag)
      ?.shadowRoot
      ?.querySelector(tabElementQueryString(config, 'extensionTab'))

    root
      ?.querySelectorAll(tabElementQueryString(config, 'galleryTab'))
      .forEach(makeInitTab(config))
  }, 1000)
})
