import { isNil } from 'lodash'
import { TabConfig } from '../config'

import { tabElementQueryString, withPrefix, withSuffix } from '../utils/str'

import { Nullable } from '../utils/types'

import { isNotNil } from './guards'

export type TabElements = Readonly<{
  progressBar: Nullable<Element>
  generateMissingThumbnailsContainer: Nullable<Element>
  imageSrcs: {
    prev: Element[]
    main: Element
    next: Element[]
  }
  buttons: {
    refresh: HTMLButtonElement
    images: HTMLButtonElement[]
    moveToThisTab: HTMLButtonElement[]
    generateThumbnails: Nullable<HTMLButtonElement>
  }
}>

const getImageSrcs = (config: TabConfig): Nullable<TabElements['imageSrcs']> => {
  const placeholder = null
  const imageSrcsAcc: TabElements['imageSrcs'] = {
    next: [],
    main: placeholder as unknown as Element,
    prev: []
  }

  const imageSrcs = Array.from(config.tabRoot.querySelectorAll(tabElementQueryString(config, 'imgSrcs')))
    .map((container) => container.querySelector('.output-html'))
    .filter(isNotNil)
    .reduce((acc, container) => {
      const containerId = container.id

      if (containerId.includes('0')) {
        acc.main = container
      }

      if (/-\d+/.test(containerId)) {
        acc.prev.push(container)
      } else {
        acc.next.push(container)
      }

      return acc
    }, imageSrcsAcc)

  if (imageSrcs.main === placeholder) {
    return null
  }

  return imageSrcs
}

const getMoveToThisTabButtons = (config: TabConfig): HTMLButtonElement[] => {
  return config.otherTabs
    .map((otherTab) => {
      const query = tabElementQueryString(config, 'moveToButton', withPrefix(otherTab.tabId, config.tabId))
      return config.appRoot.querySelector<HTMLButtonElement>(query)
    })
    .filter(isNotNil)
}

const getRefreshButton = (config: TabConfig): Nullable<HTMLButtonElement> => {
  return config.tabRoot.querySelector<HTMLButtonElement>(tabElementQueryString(config, 'hiddenRefreshButton'))
}

const getImageButtons = (config: TabConfig): HTMLButtonElement[] => {
  return Array.from(config.tabRoot.querySelectorAll(tabElementQueryString(config, 'imgButton')))
}

const getProgressBar = (config: TabConfig): Nullable<Element> => {
  const id = `#${withSuffix(config.suffixes.progressBar, config.tabId)}`

  // ¯\_(ツ)_/¯
  return config.appRoot.querySelector(id)?.querySelector(id)
}

const getGenerateMissingThumbnailsButton = (config: TabConfig): Nullable<HTMLButtonElement> => {
  return config.appRoot.querySelector<HTMLButtonElement>(`#${withPrefix(config.suffixes.generateThumbnailsButton, config.extensionId)}`)
}

const getGenerateMissingThumbnailsContainer = (config: TabConfig): Nullable<HTMLButtonElement> => {
  return config.appRoot.querySelector<HTMLButtonElement>(`#${withPrefix(config.suffixes.generateThumbnailsContainer, config.extensionId)}`)
}

const getElements = (config: TabConfig): Nullable<TabElements> => {
  const imageButtons = getImageButtons(config)
  const refreshButton = getRefreshButton(config)
  const moveToThisTabButtons = getMoveToThisTabButtons(config)
  const progressBar = getProgressBar(config)
  const generateThumbnailsButton = getGenerateMissingThumbnailsButton(config)
  const generateThumbnailsContainer = getGenerateMissingThumbnailsContainer(config)

  const imageSrcs = getImageSrcs(config)

  if (isNil(refreshButton) || isNil(imageSrcs)) {
    return null
  }

  return {
    buttons: {
      images: imageButtons,
      refresh: refreshButton,
      moveToThisTab: moveToThisTabButtons,
      generateThumbnails: generateThumbnailsButton
    },
    generateMissingThumbnailsContainer: generateThumbnailsContainer,
    imageSrcs,
    progressBar
  }
}

export default getElements
