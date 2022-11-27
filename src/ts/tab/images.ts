import { isNil, negate, nth } from 'lodash'
import { isEmpty } from './guards'

export const extractImageSrcs = (element: Element): string[] => {
  return element.innerHTML.split('\n').filter(negate(isEmpty)).map((src) => `file=${src}`)
}

type ImagesElements = HTMLImageElement[]

export const insertImagesIntoButtons = (imagesSources: string[], buttons: Element[]): ImagesElements => {
  return buttons.map((button, index) => {
    button.innerHTML = ''
    const imageSrc = nth(imagesSources, index)

    const imageTag = document.createElement('img')
    imageTag.src = imageSrc ?? ''

    button.appendChild(imageTag)

    return imageTag
  })
}

export const makeChangeImagesVisiblity = (shouldBeVisible: boolean, images: ImagesElements) => () => {
  images.forEach((image) => {
    if (!isNil(image)) {
      image.style.opacity = shouldBeVisible ? '1' : '0'
    }
  })
}

export const makeUpdateImages = (
  listener: (imageIndex: number) => void
) => async (newImagesSources: string[], images: ImagesElements) => {
  if (isEmpty(newImagesSources)) {
    return false
  }

  images.forEach((image, i) => {
    const source = newImagesSources[i]

    if (!isNil(source)) {
      image.src = source
      image.onload = () => listener(i)
    } else {
      image.src = 'about:blank'
      listener(i)
    }
  })

  return true
}

type PreloadImages = (root: Element, imageSrcs: string[]) => void

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
