import { debounce, isNil } from 'lodash'

import { TabConfig } from '../../config/types'
import { TabElements } from '../../elements/tab'

import { call, invoke } from '../../utils/fn'
import { Nullable } from '../../utils/types'
import { extractImageSrcs, PreloadImages } from '../dom/images'

import {
  makeGenerateThumbnailsListener,
  makeImageSourcesListener,
  makeProgressBarListener,
  makeSelectedImageListener,
  makePageChangeListener,
  PageChangeCallback,
  SelectedImageCallback,
  ImageSourcesCallback
} from './listeners'

type MultipleListeners<T> = T[]
type OnDoneListener = () => void

const makeMainPageSourceObserver = (config: TabConfig, elements: TabElements) => (
  onSrcChange: MultipleListeners<ImageSourcesCallback>
): MutationObserver => {
  const observer = new MutationObserver(makeImageSourcesListener((value) => {
    onSrcChange.forEach(call(value))
  }))

  observer.observe(elements.imageSrcs.main, { childList: true })
  return observer
}

const makePreloadedPagesSourceObservers = (config: TabConfig, elements: TabElements) => (
  preloadImages: MultipleListeners<PreloadImages>
): MutationObserver[] => {
  return [...elements.imageSrcs.prev, ...elements.imageSrcs.next].map((imageSrcNode) => {
    preloadImages.forEach(call(extractImageSrcs(imageSrcNode)))

    const observer = new MutationObserver(makeImageSourcesListener(debounce(async (element) => {
      preloadImages.forEach(call(extractImageSrcs(element)))
    }, config.staticConfig.debounceMs)))

    observer.observe(imageSrcNode, { childList: true })
    return observer
  })
}

const makeProgressBarObserver = (config: TabConfig, elements: TabElements) => (
  onDone: MultipleListeners<OnDoneListener>
): Nullable<MutationObserver> => {
  if (isNil(elements.progressBar)) {
    return null
  }

  const observer = new MutationObserver(makeProgressBarListener((done) => {
    if (done) {
      onDone.forEach(invoke)
    }
  }))

  observer.observe(elements.progressBar, { childList: true })
  return observer
}

const makeSelectedImageObserver = (config: TabConfig, elements: TabElements) => (
  onChange: MultipleListeners<SelectedImageCallback>
): MutationObserver => {
  const observer = new MutationObserver(makeSelectedImageListener((value) => {
    onChange.forEach(call(value))
  }))

  observer.observe(elements.imageSrcs.selected, { attributes: true })
  return observer
}

const makeGenerateThumbnailsObserver = (config: TabConfig, elements: TabElements) => (
  onDone: MultipleListeners<OnDoneListener>
): Nullable<MutationObserver> => {
  if (isNil(elements.generateMissingThumbnailsContainer)) {
    return null
  }

  const observer = new MutationObserver(makeGenerateThumbnailsListener(config, (done) => {
    if (done) {
      onDone.forEach(invoke)
      observer.disconnect()
    }
  }))

  observer.observe(elements.generateMissingThumbnailsContainer, { attributes: true, attributeFilter: ['class'] })
  return observer
}

const makePageChangeObserver = (config: TabConfig, elements: TabElements) => (
  onPageChange: MultipleListeners<PageChangeCallback>
): MutationObserver => {
  const observer = new MutationObserver(makePageChangeListener((index) => {
    onPageChange.forEach(call(index))
  }))

  observer.observe(elements.navigation.index, { childList: true })
  return observer
}

type Observers = Readonly<{
  mainPageSource: ReturnType<typeof makeMainPageSourceObserver>
  preloadedPagesSources: ReturnType<typeof makePreloadedPagesSourceObservers>
  progressBarObserver: ReturnType<typeof makeProgressBarObserver>
  generateThumbnailsObserver: ReturnType<typeof makeGenerateThumbnailsObserver>
  selectedImageObserver: ReturnType<typeof makeSelectedImageObserver>
  pageChangeObserver: ReturnType<typeof makePageChangeObserver>
}>

const setupObservers = (config: TabConfig, elements: TabElements): Observers => {
  return {
    mainPageSource: makeMainPageSourceObserver(config, elements),
    preloadedPagesSources: makePreloadedPagesSourceObservers(config, elements),
    progressBarObserver: makeProgressBarObserver(config, elements),
    generateThumbnailsObserver: makeGenerateThumbnailsObserver(config, elements),
    selectedImageObserver: makeSelectedImageObserver(config, elements),
    pageChangeObserver: makePageChangeObserver(config, elements)
  }
}

export default setupObservers
