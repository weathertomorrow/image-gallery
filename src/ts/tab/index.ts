import { isNil } from 'lodash'

import { TabConfig } from '../config/types'
import { contains } from '../utils/dom'
import { Keys, onKey } from '../utils/events'
import { flow, prop, withEffect } from '../utils/fn'

import { extractGridDimensions, updateGridCssVariables } from './dom/grid'
import { extractImageSrcs, insertImagesIntoButtons, makeChangeImagesVisiblity, makePreloadImages, makeUpdateImages } from './dom/images'
import { makeBigPictureModeHandlers, makeClickSiblingToSelectedImage, makeOnMainPageSourcesChanged, makeShowLoading, makeUpdateGalleryModes, makeUpdateSelection } from './dom/updates'
import { emitClick, makeEmitClick } from './events/emitters'
import { makeHTMLEventListener, makeImageLoadListener } from './events/listeners'
import setupObservers from './events/observers'
import { ifInBigPictureMode, ifTabActive, isTabActive, makeIsSelectedButton } from './utils'

export const initTab = (config: TabConfig): void => {
  const { tabElements, tabInfo, externalElements } = config

  const gridDimensions = withEffect(extractGridDimensions(tabElements.buttons.images ?? []), updateGridCssVariables)
  const imagesPerPage = gridDimensions.columns * gridDimensions.rows

  const observers = setupObservers(config, tabElements)
  const images = insertImagesIntoButtons(extractImageSrcs(tabElements.imageSrcs.main), tabElements.buttons.images)

  const refresh = makeEmitClick(tabElements.buttons.refresh)
  const hideImages = makeChangeImagesVisiblity(false, images)
  const showImages = makeChangeImagesVisiblity(true, images)

  const { reset: resetLoadingPrevPage, listen: aggregatedLoadListener } = makeImageLoadListener({
    imagesPerPage,
    onDone: showImages,
    onReset: hideImages
  })

  const selection = makeUpdateSelection(config, tabElements)
  const bigPicture = makeBigPictureModeHandlers(config, tabElements)

  observers.mainPageSource([makeOnMainPageSourcesChanged(config, images, resetLoadingPrevPage, makeUpdateImages(aggregatedLoadListener, selection.onPageChange))])
  observers.preloadedPagesSources([makePreloadImages(config.runtimeConfig.preloadRoot)])
  observers.progressBarObserver([refresh])
  observers.generateThumbnailsObserver([refresh])
  observers.selectedImageObserver([makeUpdateGalleryModes(config, tabElements, makeHTMLEventListener('click', bigPicture.open)), selection.onImageChange, bigPicture.update])

  externalElements.moveToThisTabButtons.forEach(makeHTMLEventListener('click', refresh))
  tabElements.buttons.generateThumbnails?.addEventListener('click', makeShowLoading(config, tabElements.buttons.generateThumbnails))
  tabElements.buttons.images.forEach(makeHTMLEventListener('click', bigPicture.open, makeIsSelectedButton(tabElements)))
  config.runtimeConfig.bigPictureRoot.addEventListener('click', bigPicture.close)

  window.addEventListener('keydown', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowDown], makeClickSiblingToSelectedImage('next', tabElements))))
  window.addEventListener('keydown', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowUp], makeClickSiblingToSelectedImage('previous', tabElements))))
  window.addEventListener('keydown', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowLeft], makeEmitClick(tabElements.navigation.buttons.prevPage))))
  window.addEventListener('keydown', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowRight], makeEmitClick(tabElements.navigation.buttons.nextPage))))
  window.addEventListener('keydown', ifTabActive(config.runtimeConfig, onKey([Keys.Esc], ifInBigPictureMode(config.runtimeConfig, {
    if: bigPicture.close,
    else: makeEmitClick(tabElements.buttons.deselectImage)
  }))))

  if (!isNil(tabInfo.keybind)) {
    window.addEventListener('keydown', onKey([tabInfo.keybind], () => {
      externalElements.moveToThisTabButtons.forEach((button) => {
        const containingTab = config.otherTabs.find(flow(prop('runtimeConfig'), prop('tabRoot'), contains(button)))

        if (!isNil(containingTab) && isTabActive(containingTab.runtimeConfig) && !isNil(containingTab.tabElements.MUTABLE.selectedImage)) {
          emitClick(button)
        }
      })
    }))
  }
}
