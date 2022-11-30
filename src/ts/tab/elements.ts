import { first, isEmpty, isNil, last } from 'lodash'
import { TabConfig } from '../config'

import { tabElementQueryString, withPrefix, withSuffix } from '../utils/str'
import { Nullable } from '../utils/types'
import { isNotNil } from '../utils/guards'

export const getFirstImageInTab = (tabElements: TabElements): Nullable<HTMLButtonElement> => first(tabElements.buttons.images)
export const getLastImageInTab = (tabElements: TabElements): Nullable<HTMLButtonElement> => last(tabElements.buttons.images)

export type TabElements = Readonly<{
  progressBar: Nullable<Element>
  generateMissingThumbnailsContainer: Nullable<Element>
  imageSrcs: {
    selected: HTMLTextAreaElement
    prev: Element[]
    main: Element
    next: Element[]
  }
  navigation: {
    buttons: {
      firstPage: HTMLButtonElement
      prevPage: HTMLButtonElement
      nextPage: HTMLButtonElement
      lastPage: HTMLButtonElement
    }
    index: Element
  }
  gallery: {
    container: Element
    gallery: Element
  }
  buttons: {
    refresh: HTMLButtonElement
    images: HTMLButtonElement[]
    moveToThisTab: HTMLButtonElement[]
    generateThumbnails: Nullable<HTMLButtonElement>
  }
}>

const getPageIndex = (config: TabConfig): Nullable<Element> => {
  const queryString = tabElementQueryString(config, 'hiddenPageIndex')
  return config.tabRoot.querySelector(queryString)?.querySelector(queryString)
}

const getNavigation = (config: TabConfig): Nullable<TabElements['navigation']> => {
  const pageIndex = getPageIndex(config)

  if (isNil(pageIndex)) {
    return null
  }

  const buttons = Array.from(config.tabRoot.querySelector(tabElementQueryString(config, 'navigationControllsContainer'))
    ?.querySelectorAll('button') ?? [])

  if (isEmpty(buttons) || buttons.length !== 4) {
    return null
  }

  const [firstPage, prevPage, nextPage, lastPage] = buttons

  return {
    buttons: {
      firstPage,
      prevPage,
      nextPage,
      lastPage
    },
    index: pageIndex
  }
}

const getSelectedImagePath = (config: TabConfig): Nullable<HTMLTextAreaElement> => {
  return config.tabRoot.querySelector(tabElementQueryString(config, 'selectedImagePath'))
    ?.querySelector('textarea')
}

const getImageSrcs = (config: TabConfig): Nullable<TabElements['imageSrcs']> => {
  const placeholder = null
  const selectedImage = getSelectedImagePath(config)

  if (isNil(selectedImage)) {
    return null
  }

  const imageSrcsAcc: TabElements['imageSrcs'] = {
    next: [],
    main: placeholder as unknown as Element,
    prev: [],
    selected: selectedImage
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
  return config.tabRoot.querySelector<HTMLButtonElement>(tabElementQueryString(config, 'refreshButton'))
}

const getImageButtons = (config: TabConfig): HTMLButtonElement[] => {
  return Array.from(config.tabRoot.querySelectorAll(tabElementQueryString(config, 'imgButton')))
}

const getProgressBar = (config: TabConfig): Nullable<Element> => {
  const id = `#${withSuffix(config.suffixes.progressBar, config.tabId)}`

  // ¯\_(ツ)_/¯
  return config.appRoot.querySelector(id)?.querySelector(id)
}

const getGallery = (config: TabConfig): Nullable<Element> => {
  return config.tabRoot.querySelector(tabElementQueryString(config, 'gallery'))
}

const getGalleryContainer = (config: TabConfig): Nullable<Element> => {
  return config.tabRoot.querySelector(tabElementQueryString(config, 'galleryContainer'))
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
  const gallery = getGallery(config)
  const galleryContainer = getGalleryContainer(config)
  const navigation = getNavigation(config)

  if (isNil(refreshButton) || isNil(imageSrcs) || isNil(gallery) || isNil(galleryContainer) || isNil(navigation)) {
    return null
  }

  return {
    gallery: {
      gallery,
      container: galleryContainer
    },
    buttons: {
      images: imageButtons,
      refresh: refreshButton,
      moveToThisTab: moveToThisTabButtons,
      generateThumbnails: generateThumbnailsButton
    },
    generateMissingThumbnailsContainer: generateThumbnailsContainer,
    imageSrcs,
    progressBar,
    navigation
  }
}

export default getElements
