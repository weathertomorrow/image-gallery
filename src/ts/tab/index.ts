import { isEmpty, isNil } from 'lodash'
import { Config } from '../config'
import { withEffect } from '../utils/fn'
import { tabElementQueryString } from '../utils/str'
import { Nullable } from '../utils/types'
import { extractGridDimensions, updateGridCssVariables } from './grid'
import { extractImageSrcs, insertImagesIntoButtons, makeUpdateImages, makeChangeImagesVisiblity, MakeUpdateImagesReturnValue } from './images'

type TabElements = Readonly<{
  imageSrcs: Element
  buttons: Element[]
}>

const getElements = (config: Config, tabRoot: Element): Nullable<TabElements> => {
  const imageSrcs = tabRoot.querySelector(tabElementQueryString(config, 'imgSrcs'))?.querySelector('.output-html')
  const buttons = Array.from(tabRoot.querySelectorAll(tabElementQueryString(config, 'imgButton')))

  return isNil(imageSrcs) ? null : { imageSrcs, buttons }
}

const makeImageSourcesObserver = (callback: (node: Element) => void): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation

  if (!isNil(target) && target instanceof Element) {
    callback(target)
  }
}

type MakeImagesLoadListenerArg = Readonly<{
  imagesPerPage: number
  onDone: () => void
  onReset: () => void
}>

type MakeImagesLoadListenerReturnValue = Readonly<{
  reset: () => void
  listen: () => void
}>

const makeImageLoadListener = ({
  imagesPerPage,
  onDone,
  onReset
}: MakeImagesLoadListenerArg): MakeImagesLoadListenerReturnValue => {
  let progress = imagesPerPage

  return {
    reset: () => {
      onReset()
      progress = imagesPerPage
    },
    listen: () => {
      progress = Math.max(0, progress - 1)

      if (progress === 0) {
        onDone()
      }
    }
  }
}

export const makeInitTab = (config: Config) => (tabRoot: Element): void => {
  const elements = getElements(config, tabRoot)

  if (isNil(elements)) {
    return
  }

  const gridDimensions = withEffect(extractGridDimensions(elements?.buttons ?? []), updateGridCssVariables)
  const imagesPerPage = gridDimensions.columns * gridDimensions.rows

  const images = insertImagesIntoButtons(extractImageSrcs(elements.imageSrcs), elements.buttons)
  const hideImages = makeChangeImagesVisiblity(false, images)
  const showImages = makeChangeImagesVisiblity(true, images)

  const { reset, listen: aggregatedLoadListener } = makeImageLoadListener({
    imagesPerPage,
    onDone: showImages,
    onReset: hideImages
  })

  let shouldCancelPrevRef: MakeUpdateImagesReturnValue['shouldCancel'] = { current: false }

  const observer = new MutationObserver(makeImageSourcesObserver((element) => {
    shouldCancelPrevRef.current = true

    const { shouldCancel, updateImages } = makeUpdateImages(aggregatedLoadListener)
    shouldCancelPrevRef = shouldCancel

    reset()
    updateImages(extractImageSrcs(element), images)
  }))

  observer.observe(elements.imageSrcs, { childList: true })
}
