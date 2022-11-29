import { isArray, isNil, negate, nth } from 'lodash'
import { Nullable } from '../utils/types'
import { isArrayOf, isEmpty, isImagePathData } from './guards'

export type ParsedImage = Readonly<{
  image: string
  thumbnail: Nullable<string>
}>

const toLocalImagePath = (imgPath: string): string => `file=${imgPath}`

export const extractImageSrcs = (element: Element): ParsedImage[] => {
  if (isEmpty(element.innerHTML)) {
    return []
  }

  const parsedJson = JSON.parse(element.innerHTML)
  const data = isArray(parsedJson) ? parsedJson.filter(negate(isEmpty)) : parsedJson
  console.log(data)
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
    imageTag.src = imageSrc?.image ?? ''

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
  listener: (imageIndex: number) => void
): UpdateImages => async (newImagesSources, images) => {
  if (isEmpty(newImagesSources)) {
    return false
  }

  images.forEach((image, i) => {
    const source = newImagesSources[i]

    if (!isNil(source)) {
      markImageAsNormal(image)
      image.src = source.image
      image.onload = () => listener(i)
    } else {
      markImageAsPermanentlyHidden(image)
      listener(i)
    }
  })

  return true
}

export type PreloadImages = (imageSrcs: ParsedImage[]) => void
export const makePreloadImages = (root: Element): PreloadImages => {
  const alreadyPreloaded = new Map<string, null>()

  return (imageSrcs: ParsedImage[]): void => {
    imageSrcs.forEach((imageSrc) => {
      if (alreadyPreloaded.has(imageSrc.image)) {
        return
      }

      alreadyPreloaded.set(imageSrc.image, null)
      const imageTag = document.createElement('img')

      imageTag.src = imageSrc.image
      imageTag.hidden = true

      root.appendChild(imageTag)
    })
  }
}
