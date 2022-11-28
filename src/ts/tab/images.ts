import { isNil, negate, nth } from 'lodash'
import { isEmpty } from './guards'

export const extractImageSrcs = (element: Element): string[] => {
  return element.innerHTML.split('\n').filter(negate(isEmpty)).map((src) => `file=${src}`)
}

export type ImagesElements = HTMLImageElement[]
export const insertImagesIntoButtons = (imagesSources: string[], buttons: Element[]): ImagesElements => {
  return buttons.map((button, index) => {
    button.innerHTML = ''

    const imageSrc = nth(imagesSources, index)
    const imageTag = document.createElement('img')
    imageTag.src = imageSrc ?? ''

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

export type UpdateImages = (newImagesSources: string[], images: ImagesElements) => Promise<boolean>
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
      image.src = source
      image.onload = () => listener(i)
    } else {
      markImageAsPermanentlyHidden(image)
      listener(i)
    }
  })

  return true
}

export type PreloadImages = (root: Element, imageSrcs: string[]) => void
export const makePreloadImages = (): PreloadImages => {
  const alreadyPreloaded = new Map<string, null>()

  return (root: Element, imageSrcs: string[]): void => {
    imageSrcs.forEach((imageSrc) => {
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
