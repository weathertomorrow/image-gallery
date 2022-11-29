import { debounce, isNil } from 'lodash'
import { TabConfig } from '../config'
import { Nullable } from '../utils/types'
import { TabElements } from './elements'
import { extractImageSrcs, ImagesElements, PreloadImages, UpdateImages } from './images'
import { makeGenerateThumbnailsListener, makeImageSourcesListener, makeProgressBarListener } from './listeners'

const makeMainPageSourceObserver = (config: TabConfig, elements: TabElements) => (
  updateImages: UpdateImages,
  resetLoading: () => void,
  images: ImagesElements
): MutationObserver => {
  const observer = new MutationObserver(makeImageSourcesListener(debounce(async (element) => {
    resetLoading()
    void updateImages(extractImageSrcs(element), images)
  }, config.debounceMs)))

  observer.observe(elements.imageSrcs.main, { childList: true })
  return observer
}

const makePreloadedPagesSourceObservers = (config: TabConfig, elements: TabElements) => (
  preloadImages: PreloadImages
): MutationObserver[] => {
  return [...elements.imageSrcs.prev, ...elements.imageSrcs.next].map((imageSrcNode) => {
    preloadImages(extractImageSrcs(imageSrcNode))

    const observer = new MutationObserver(makeImageSourcesListener(debounce(async (element) => {
      preloadImages(extractImageSrcs(element))
    }, config.debounceMs)))

    observer.observe(imageSrcNode, { childList: true })
    return observer
  })
}

const makeProgressBarObserver = (config: TabConfig, elements: TabElements) => (
  onDone: () => void
): Nullable<MutationObserver> => {
  if (isNil(elements.progressBar)) {
    return null
  }

  const observer = new MutationObserver(makeProgressBarListener((done) => {
    if (done) {
      onDone()
    }
  }))

  observer.observe(elements.progressBar, { childList: true })
  return observer
}

const makeGenerateThumbnailsObserver = (config: TabConfig, elements: TabElements) => (
  onDone: () => void
): Nullable<MutationObserver> => {
  if (isNil(elements.generateMissingThumbnailsContainer)) {
    return null
  }

  const observer = new MutationObserver(makeGenerateThumbnailsListener(config, (done) => {
    if (done) {
      onDone()
      observer.disconnect()
    }
  }))

  observer.observe(elements.generateMissingThumbnailsContainer, { attributes: true, attributeFilter: ['class'] })
  return observer
}

type Observers = Readonly<{
  mainPageSource: ReturnType<typeof makeMainPageSourceObserver>
  preloadedPagesSources: ReturnType<typeof makePreloadedPagesSourceObservers>
  progressBarObserver: ReturnType<typeof makeProgressBarObserver>
  generateThumbnailsObserver: ReturnType<typeof makeGenerateThumbnailsObserver>
}>

const setupObservers = (config: TabConfig, elements: TabElements): Observers => {
  return {
    mainPageSource: makeMainPageSourceObserver(config, elements),
    preloadedPagesSources: makePreloadedPagesSourceObservers(config, elements),
    progressBarObserver: makeProgressBarObserver(config, elements),
    generateThumbnailsObserver: makeGenerateThumbnailsObserver(config, elements)
  }
}

export default setupObservers
