import { isNil, last } from 'lodash'
import { TabConfig } from '../config'
import { isEmpty } from '../utils/guards'
import { Nullable } from '../utils/types'
import { TabElements } from './elements'

export const ifTabActive = <T, U>(tab: TabConfig, fn: (arg: T) => U) => {
  return (arg: T) => {
    if (tab.runtimeConfig.tabRoot.style.display !== 'none') {
      return fn(arg)
    }
    return null
  }
}

export const getSelectedImagePath = (target: HTMLTextAreaElement): Nullable<string> => {
  const parsedValue = isEmpty(target.value) ? null : target.value
  return parsedValue
}

export const scrollToElement = (element: Nullable<Element>): void => {
  element?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
}

export const toLocalImagePath = (imgPath: string): string => `file=${imgPath}`
export const getImageNameFromPath = (imgPath: string): Nullable<string> => last(imgPath.split(/[/\\]/g))

export const findButtonForImage = (elements: TabElements, image: Nullable<string>): Nullable<HTMLElement> => {
  if (isNil(image)) {
    return null
  }

  const selectedImageName = getImageNameFromPath(image)

  if (isNil(selectedImageName)) {
    return null
  }

  return elements.buttons.images.find((buttonEl) => {
    const src = buttonEl.querySelector('img')?.src
    return !isNil(src) && (decodeURIComponent(src).includes(selectedImageName) || src.includes(selectedImageName))
  })
}

export const makeIsSelectedButton = (elements: TabElements) => (el: HTMLElement) => {
  return el === findButtonForImage(elements, elements.MUTABLE.selectedImage?.src)
}
