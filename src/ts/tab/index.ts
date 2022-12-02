import { isNil } from 'lodash'

import { TabConfig } from '../config/types'
import { makeGetSwitchToThisTabButton } from '../elements/tab'
import { contains } from '../utils/dom'
import { Keys, onKey } from '../utils/events'
import { flow, prop, withEffect, wrapped } from '../utils/fn'

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
  const bigPictureControls = makeBigPictureModeHandlers(config, tabElements)
  const switchTabKeybindArg = [{ shift: true }, wrapped(flow(makeGetSwitchToThisTabButton(config), emitClick))] as const

  observers.mainPageSource([makeOnMainPageSourcesChanged(config, images, resetLoadingPrevPage, makeUpdateImages(aggregatedLoadListener, selection.onPageChange))])
  observers.preloadedPagesSources([makePreloadImages(config.runtimeConfig.preloadRoot)])
  observers.progressBarObserver([refresh])
  observers.generateThumbnailsObserver([refresh])
  observers.selectedImageObserver([makeUpdateGalleryModes(config, tabElements, makeHTMLEventListener('click', bigPictureControls.open)), selection.onImageChange, bigPictureControls.update])

  externalElements.moveToThisTabButtons.forEach(makeHTMLEventListener('click', refresh))
  tabElements.buttons.generateThumbnails?.addEventListener('click', makeShowLoading(config, tabElements.buttons.generateThumbnails))
  config.runtimeConfig.bigPictureRoot.addEventListener('click', bigPictureControls.close)
  tabElements.buttons.images.forEach(makeHTMLEventListener('click', ifInBigPictureMode(config.runtimeConfig, bigPictureControls), makeIsSelectedButton(tabElements)))

  window.addEventListener('keyup', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowDown], makeClickSiblingToSelectedImage('next', tabElements))))
  window.addEventListener('keyup', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowUp], makeClickSiblingToSelectedImage('previous', tabElements))))
  window.addEventListener('keyup', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowLeft], makeEmitClick(tabElements.navigation.buttons.prevPage))))
  window.addEventListener('keyup', ifTabActive(config.runtimeConfig, onKey([Keys.ArrowRight], makeEmitClick(tabElements.navigation.buttons.nextPage))))
  window.addEventListener('keyup', ifTabActive(config.runtimeConfig, onKey([Keys.Esc], ifInBigPictureMode(config.runtimeConfig, {
    if: bigPictureControls.close,
    else: makeEmitClick(tabElements.buttons.deselectImage)
  }))))
  window.addEventListener('keyup', onKey([tabInfo.keybind, `${config.index + 1}`], ...switchTabKeybindArg))
  window.addEventListener('keyup', onKey([tabInfo.keybind], { shift: false }, () => {
    externalElements.moveToThisTabButtons.forEach((button) => {
      const containingTab = config.otherTabs.find(flow(prop('runtimeConfig'), prop('tabRoot'), contains(button)))

      if (!isNil(containingTab) && isTabActive(containingTab.runtimeConfig) && !isNil(containingTab.tabElements.MUTABLE.selectedImage)) {
        emitClick(button)
      }
    })
  }))
}
