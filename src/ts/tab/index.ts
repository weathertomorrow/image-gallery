import { debounce, isNil } from 'lodash'

import { Config } from '../config'

import { tabElementQueryString } from '../utils/str'
import { withEffect } from '../utils/fn'
import { Nullable } from '../utils/types'

import { isNotNil } from './guards'
import { extractGridDimensions, updateGridCssVariables } from './grid'
import { makeImageLoadListener, makeImageSourcesObserver } from './listeners'
import { extractImageSrcs, insertImagesIntoButtons, makeUpdateImages, makeChangeImagesVisiblity, makePreloadImages } from './images'

type TabElements = Readonly<{
  imageSrcs: {
    prev: Element[]
    main: Element
    next: Element[]
  }
  buttons: Element[]
}>

const getElements = (config: Config, tabRoot: Element): Nullable<TabElements> => {
  const placeholder = null
  const imageSrcsAcc: TabElements['imageSrcs'] = {
    next: [],
    main: placeholder as unknown as Element,
    prev: []
  }

  const buttons = Array.from(tabRoot.querySelectorAll(tabElementQueryString(config, 'imgButton')))
  const imageSrcs = Array.from(tabRoot.querySelectorAll(tabElementQueryString(config, 'imgSrcs')))
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

  return { buttons, imageSrcs }
}

export const makeInitTab = (config: Config, preloadRoot: Element) => (tabRoot: Element): void => {
  const elements = getElements(config, tabRoot)

  if (isNil(elements)) {
    return
  }

  const gridDimensions = withEffect(extractGridDimensions(elements?.buttons ?? []), updateGridCssVariables)
  const imagesPerPage = gridDimensions.columns * gridDimensions.rows

  const images = insertImagesIntoButtons(extractImageSrcs(elements.imageSrcs.main), elements.buttons)
  const preloadImages = makePreloadImages()
  const hideImages = makeChangeImagesVisiblity(false, images)
  const showImages = makeChangeImagesVisiblity(true, images)

  const { reset: resetLoadingPrevPage, listen: aggregatedLoadListener } = makeImageLoadListener({
    imagesPerPage,
    onDone: showImages,
    onReset: hideImages
  })
  const updateImages = makeUpdateImages(aggregatedLoadListener)

  new MutationObserver(makeImageSourcesObserver(debounce(async (element) => {
    resetLoadingPrevPage()
    void updateImages(extractImageSrcs(element), images)
  }, config.debounceMs))).observe(elements.imageSrcs.main, { childList: true });

  [...elements.imageSrcs.prev, ...elements.imageSrcs.next].forEach((imageSrcNode) => {
    preloadImages(preloadRoot, extractImageSrcs(imageSrcNode))

    new MutationObserver(makeImageSourcesObserver(debounce(async (element) => {
      preloadImages(preloadRoot, extractImageSrcs(element))
    }, config.debounceMs))).observe(imageSrcNode, { childList: true })
  })
}
