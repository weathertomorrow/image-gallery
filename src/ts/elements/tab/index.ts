import { isEmpty, isNil } from 'lodash'

import { BaseTabConfig } from '../../config/types'

import { isNotNil } from '../../utils/guards'
import { withPrefix, withSuffix } from '../../utils/str'
import { MutableObject, Nullable } from '../../utils/types'

import { tabElementQueryString } from './utils'

export type TabElements = Readonly<{
  progressBar: Nullable<Element>
  tabInfo: Element
  generateMissingThumbnailsContainer: Nullable<Element>
  imageSrcs: Readonly< {
    selected: HTMLTextAreaElement
    prev: Element[]
    main: Element
    next: Element[]
  }>
  navigation: Readonly<{
    buttons: Readonly<{
      firstPage: HTMLButtonElement
      prevPage: HTMLButtonElement
      nextPage: HTMLButtonElement
      lastPage: HTMLButtonElement
    }>
    index: Element
  }>
  gallery: Readonly< {
    container: Element
    gallery: Element
  }>
  buttons: Readonly< {
    refresh: HTMLButtonElement
    images: HTMLButtonElement[]
    generateThumbnails: Nullable<HTMLButtonElement>
    deselectImage: HTMLButtonElement
  }>
  MUTABLE: {
    selectedImage: Nullable<HTMLImageElement>
    bigPictureImage: Nullable<HTMLImageElement>
  }
}>

const getTabInfo = (config: BaseTabConfig): Nullable<Element> => {
  const queryString = tabElementQueryString(config.staticConfig, 'hiddenTabInfo')
  return config.runtimeConfig.tabRoot.querySelector(queryString)?.querySelector(queryString)
}

const getPageIndex = (config: BaseTabConfig): Nullable<Element> => {
  const queryString = tabElementQueryString(config.staticConfig, 'hiddenPageIndex')
  return config.runtimeConfig.tabRoot.querySelector(queryString)?.querySelector(queryString)
}

const getNavigation = (config: BaseTabConfig): Nullable<TabElements['navigation']> => {
  const pageIndex = getPageIndex(config)

  if (isNil(pageIndex)) {
    return null
  }

  const buttons = Array.from(config.runtimeConfig.tabRoot.querySelector(tabElementQueryString(config.staticConfig, 'navigationControllsContainer'))
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

const getSelectedImagePath = (config: BaseTabConfig): Nullable<HTMLTextAreaElement> => {
  return config.runtimeConfig.tabRoot.querySelector(tabElementQueryString(config.staticConfig, 'selectedImagePath'))
    ?.querySelector('textarea')
}

const getImageSrcs = (config: BaseTabConfig): Nullable<TabElements['imageSrcs']> => {
  const placeholder = null
  const selectedImage = getSelectedImagePath(config)

  if (isNil(selectedImage)) {
    return null
  }

  const imageSrcsAcc: MutableObject<TabElements['imageSrcs']> = {
    next: [],
    main: placeholder as unknown as Element,
    prev: [],
    selected: selectedImage
  }

  const imageSrcs = Array.from(config.runtimeConfig.tabRoot.querySelectorAll(tabElementQueryString(config.staticConfig, 'imgSrcs')))
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

const getRefreshButton = (config: BaseTabConfig): Nullable<HTMLButtonElement> => {
  return config.runtimeConfig.tabRoot.querySelector<HTMLButtonElement>(tabElementQueryString(config.staticConfig, 'refreshButton'))
}

const getImageButtons = (config: BaseTabConfig): HTMLButtonElement[] => {
  return Array.from(config.runtimeConfig.tabRoot.querySelectorAll(tabElementQueryString(config.staticConfig, 'imgButton')))
}

const getProgressBar = (config: BaseTabConfig): Nullable<Element> => {
  const id = `#${withSuffix(config.staticConfig.suffixes.progressBar, config.runtimeConfig.tabId)}`

  // ¯\_(ツ)_/¯
  return config.runtimeConfig.appRoot.querySelector(id)?.querySelector(id)
}

const getGallery = (config: BaseTabConfig): Nullable<Element> => {
  return config.runtimeConfig.tabRoot.querySelector(tabElementQueryString(config.staticConfig, 'gallery'))
}

const getGalleryContainer = (config: BaseTabConfig): Nullable<Element> => {
  return config.runtimeConfig.tabRoot.querySelector(tabElementQueryString(config.staticConfig, 'galleryContainer'))
}

const getGenerateMissingThumbnailsButton = (config: BaseTabConfig): Nullable<HTMLButtonElement> => {
  return config.runtimeConfig.appRoot.querySelector<HTMLButtonElement>(`#${withPrefix(config.staticConfig.suffixes.generateThumbnailsButton, config.staticConfig.extensionId)}`)
}

const getGenerateMissingThumbnailsContainer = (config: BaseTabConfig): Nullable<HTMLButtonElement> => {
  return config.runtimeConfig.appRoot.querySelector<HTMLButtonElement>(`#${withPrefix(config.staticConfig.suffixes.generateThumbnailsContainer, config.staticConfig.extensionId)}`)
}

const getDeselectImageButton = (config: BaseTabConfig): Nullable<HTMLButtonElement> => {
  return config.runtimeConfig.tabRoot.querySelector<HTMLButtonElement>(tabElementQueryString(config.staticConfig, 'deselectImageButton'))
}

export const getElements = (config: BaseTabConfig): Nullable<TabElements> => {
  const imageButtons = getImageButtons(config)
  const refreshButton = getRefreshButton(config)
  const progressBar = getProgressBar(config)
  const generateThumbnailsButton = getGenerateMissingThumbnailsButton(config)
  const generateThumbnailsContainer = getGenerateMissingThumbnailsContainer(config)
  const imageSrcs = getImageSrcs(config)
  const gallery = getGallery(config)
  const galleryContainer = getGalleryContainer(config)
  const navigation = getNavigation(config)
  const tabInfo = getTabInfo(config)
  const deselectImageButton = getDeselectImageButton(config)

  if (isNil(refreshButton) || isNil(imageSrcs) || isNil(gallery) || isNil(galleryContainer) || isNil(navigation) || isNil(tabInfo) || isNil(deselectImageButton)) {
    return null
  }

  return {
    tabInfo,
    gallery: {
      gallery,
      container: galleryContainer
    },
    buttons: {
      images: imageButtons,
      refresh: refreshButton,
      generateThumbnails: generateThumbnailsButton,
      deselectImage: deselectImageButton
    },
    generateMissingThumbnailsContainer: generateThumbnailsContainer,
    imageSrcs,
    progressBar,
    navigation,
    MUTABLE: {
      // these are created while the app is running, don't exist on load
      bigPictureImage: null,
      selectedImage: null
    }
  }
}
