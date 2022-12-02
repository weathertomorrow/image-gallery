import { isNil, last } from 'lodash'

import { RuntimeConfig } from '../config/types'
import { TabElements } from '../elements/tab'
import { isEmpty } from '../utils/guards'
import { Nullable } from '../utils/types'

export const isTabActive = (runtimeConfig: RuntimeConfig): boolean => runtimeConfig.tabRoot.style.display !== 'none'
export const isInBigPictureMode = (runtimeConfig: RuntimeConfig): boolean => runtimeConfig.bigPictureRoot.children.length !== 0

export const ifTabActive = <T, U>(runtimeConfig: RuntimeConfig, fn: (arg: T) => U) => {
  return (arg: T) => {
    if (isTabActive(runtimeConfig)) {
      return fn(arg)
    }
    return null
  }
}

type IfInBigPictureModeArg = Readonly<{
  if: () => void
  else: () => void
}>

export const ifInBigPictureMode = (runtimeConfig: RuntimeConfig, callbacks: IfInBigPictureModeArg) => {
  return () => {
    if (isInBigPictureMode(runtimeConfig)) {
      return callbacks.if()
    } else {
      return callbacks.else()
    }
  }
}

export const getSelectedImagePath = (target: HTMLTextAreaElement): Nullable<string> => {
  const parsedValue = isEmpty(target.value) ? null : target.value
  return parsedValue
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
