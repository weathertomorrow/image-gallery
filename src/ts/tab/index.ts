import { isNil } from 'lodash'

import { TabConfig } from '../config'

import { withEffect } from '../utils/fn'

import getElements from './elements'
import setupObservers from './observers'

import { extractGridDimensions, updateGridCssVariables } from './grid'
import { makeHTMLEventListener, makeImageLoadListener } from './listeners'
import { makeEmitClick } from './events'
import { extractImageSrcs, insertImagesIntoButtons, makeUpdateImages, makeChangeImagesVisiblity, makePreloadImages } from './images'
import { makeBigPictureModeHandlers, makeClickSiblingToSelectedImage, makeOnMainPageSourcesChanged, makeShowLoading, makeUpdateGalleryModes, makeUpdateSelection } from './domUpdates'
import { Keys, onKey } from '../utils/events'
import { ifTabActive, makeIsSelectedButton } from './utils'

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

  const selection = makeUpdateSelection(config, elements)
  const bigPicture = makeBigPictureModeHandlers(config, elements)

  observers.mainPageSource([makeOnMainPageSourcesChanged(config, images, resetLoadingPrevPage, makeUpdateImages(aggregatedLoadListener, selection.onPageChange))])
  observers.preloadedPagesSources([makePreloadImages(config.runtimeConfig.preloadRoot)])
  observers.progressBarObserver([refresh])
  observers.generateThumbnailsObserver([refresh])
  observers.selectedImageObserver([makeUpdateGalleryModes(config, elements, makeHTMLEventListener('click', bigPicture.open)), selection.onImageChange, bigPicture.update])

  elements.buttons.moveToThisTab.forEach(makeHTMLEventListener('click', refresh))
  elements.buttons.generateThumbnails?.addEventListener('click', makeShowLoading(config, elements.buttons.generateThumbnails))
  elements.buttons.images.forEach(makeHTMLEventListener('click', bigPicture.open, makeIsSelectedButton(elements)))

  window.addEventListener('keydown', ifTabActive(config, onKey([Keys.ArrowDown], makeClickSiblingToSelectedImage('next', elements))))
  window.addEventListener('keydown', ifTabActive(config, onKey([Keys.ArrowUp], makeClickSiblingToSelectedImage('previous', elements))))
  window.addEventListener('keydown', ifTabActive(config, onKey([Keys.ArrowLeft], makeEmitClick(elements.navigation.buttons.prevPage))))
  window.addEventListener('keydown', ifTabActive(config, onKey([Keys.ArrowRight], makeEmitClick(elements.navigation.buttons.nextPage))))
  window.addEventListener('keydown', ifTabActive(config, onKey([Keys.Esc], bigPicture.close)))
}
