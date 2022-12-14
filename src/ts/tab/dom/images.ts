import { isArray, isNil, negate, nth } from 'lodash'

import { isArrayOf, isEmpty } from '../../utils/guards'
import { Nullable } from '../../utils/types'
import { DoneCallback } from '../events/listeners'
import { toLocalImagePath } from '../utils'
import { isImagePathData } from '../utils/guards'

export type ParsedImage = Readonly<{
  image: string
  thumbnail: Nullable<string>
}>

export const extractImageSrcs = (element: Element): ParsedImage[] => {
  if (isEmpty(element.innerHTML)) {
    return []
  }

  const parsedJson = JSON.parse(element.innerHTML)
  const data = isArray(parsedJson) ? parsedJson.filter(negate(isEmpty)) : parsedJson

  if (isArrayOf(data, isImagePathData)) {
    return data.map((image) => ({
      image: toLocalImagePath(image.image),
      thumbnail: isEmpty(image.thumbnail) ? null : toLocalImagePath(image.thumbnail)
    }))
  }

  return []
}

export type ImagesElements = HTMLImageElement[]
export const insertImagesIntoButtons = (imagesSources: ParsedImage[], buttons: Element[]): ImagesElements => {
  return buttons.map((button, index) => {
    button.innerHTML = ''

    const imageSrc = nth(imagesSources, index)
    const imageTag = document.createElement('img')
    imageTag.src = imageSrc?.thumbnail ?? imageSrc?.image ?? ''

    button.appendChild(imageTag)

    if (isNil(imageSrc)) {
      markImageAsPermanentlyHidden(imageTag)
      changeImageVisiblity(false, imageTag)
    }

    return imageTag
  })
}

const markImageAsPermanentlyHidden = (image: HTMLImageElement): void => image.setAttribute('data-hidden', 'true')
const markImageAsNormal = (image: HTMLImageElement): void => image.setAttribute('data-hidden', 'false')
const shouldBePermanentlyHidden = (image: HTMLImageElement): boolean => image.getAttribute('data-hidden') === 'true'

const changeImageVisiblity = (shouldBeVisible: boolean, image: HTMLImageElement): void => {
  const parentElement = image.parentElement
  if (isNil(parentElement)) return

  if (shouldBePermanentlyHidden(image)) {
    parentElement.style.display = 'none'
  } else {
    parentElement.style.display = 'inline-flex'
  }

  image.style.opacity = shouldBeVisible ? '1' : '0'
}

export const makeChangeImagesVisiblity = (shouldBeVisible: boolean, images: ImagesElements) => () => {
  images.forEach((image) => changeImageVisiblity(shouldBeVisible, image))
}

export type UpdateImages = (newImagesSources: ParsedImage[], images: ImagesElements) => Promise<boolean>
export const makeUpdateImages = (
  onImageLoadListener: (imageIndex: number) => void,
  onDoneUpdatingListener: DoneCallback
): UpdateImages => async (newImagesSources, images) => {
  images.forEach((image, i) => {
    const source = newImagesSources[i]?.thumbnail ?? newImagesSources[i]?.image

    if (!isNil(source)) {
      markImageAsNormal(image)
      image.src = source
      image.onload = () => onImageLoadListener(i)
      image.onerror = () => {
        image.src = newImagesSources[i]?.image
      }
    } else {
      markImageAsPermanentlyHidden(image)
      onImageLoadListener(i)
    }
  })

  onDoneUpdatingListener(true)

  return true
}

export type PreloadImages = (images: ParsedImage[]) => void
export const makePreloadImages = (root: Element): PreloadImages => {
  const alreadyPreloaded = new Map<string, null>()

  return (images: ParsedImage[]): void => {
    images.forEach((image) => {
      const imageSrc = image.thumbnail ?? image.image

      if (alreadyPreloaded.has(imageSrc)) {
        return
      }

      alreadyPreloaded.set(imageSrc, null)
      const imageTag = document.createElement('img')

      imageTag.src = imageSrc
      imageTag.hidden = true

      root.appendChild(imageTag)
    })
  }
}
