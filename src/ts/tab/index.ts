import { isNil } from 'lodash'

import { TabConfig } from '../config'

import { withEffect } from '../utils/fn'

import getElements from './elements'
import setupObservers from './observers'

import { extractGridDimensions, updateGridCssVariables } from './grid'
import { makeHTMLEventListener, makeImageLoadListener } from './listeners'
import { makeEmitClick } from './eventEmitters'
import { extractImageSrcs, insertImagesIntoButtons, makeUpdateImages, makeChangeImagesVisiblity, makePreloadImages } from './images'
import { makeShowLoading, makeUpdateGalleryModes, makeUpdateSelection } from './domUpdates'

export const initTab = (config: TabConfig): void => {
  const elements = getElements(config)

  if (isNil(elements)) {
    return
  }

  const gridDimensions = withEffect(extractGridDimensions(elements.buttons.images ?? []), updateGridCssVariables)
  const imagesPerPage = gridDimensions.columns * gridDimensions.rows

  const observers = setupObservers(config, elements)
  const images = insertImagesIntoButtons(extractImageSrcs(elements.imageSrcs.main), elements.buttons.images)

  const refresh = makeEmitClick(elements.buttons.refresh)
  const hideImages = makeChangeImagesVisiblity(false, images)
  const showImages = makeChangeImagesVisiblity(true, images)

  const { reset: resetLoadingPrevPage, listen: aggregatedLoadListener } = makeImageLoadListener({
    imagesPerPage,
    onDone: showImages,
    onReset: hideImages
  })

  observers.mainPageSource(makeUpdateImages(aggregatedLoadListener), resetLoadingPrevPage, images)
  observers.preloadedPagesSources([makePreloadImages(config.preloadRoot)])
  observers.progressBarObserver([refresh])
  observers.generateThumbnailsObserver([refresh])
  observers.selectedImageObserver([makeUpdateGalleryModes(config, elements), makeUpdateSelection(config, elements)])

  elements.buttons.moveToThisTab.forEach(makeHTMLEventListener(refresh))
  elements.buttons.generateThumbnails?.addEventListener('click', makeShowLoading(config, elements.buttons.generateThumbnails))
}
