import { isEmpty, isNil } from 'lodash'
import { Config } from '../config'
import { withEffect } from '../utils/fn'
import { tabElementQueryString } from '../utils/str'
import { Nullable } from '../utils/types'
import { extractGridDimensions, updateGridCssVariables } from './grid'
import { extractImageSrcs, insertImagesIntoButtons, updateImages } from './images'

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

export const makeInitTab = (config: Config) => (tabRoot: Element): void => {
  const elements = getElements(config, tabRoot)
  const gridDimensions = withEffect(extractGridDimensions(elements?.buttons ?? []), updateGridCssVariables)

  if (isNil(elements)) {
    return
  }

  const images = insertImagesIntoButtons(extractImageSrcs(elements.imageSrcs), elements.buttons)
  images.forEach((image) => {
    if (!isNil(image)) {
      image.onload = (e) => {
        console.log(e)
      }
    }
  })

  const observer = new MutationObserver(makeImageSourcesObserver((element) => updateImages(extractImageSrcs(element), images)))
  observer.observe(elements.imageSrcs, { childList: true })
}
