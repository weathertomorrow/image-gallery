import { isNil, nth } from 'lodash'
import { Nullable } from '../utils/types'

export const extractImageSrcs = (element: Element): string[] => {
  return element.innerHTML.split('\n').map((src) => `file=${src}`)
}

type ImagesElements = Array<Nullable<HTMLImageElement>>

export const insertImagesIntoButtons = (imagesSources: string[], buttons: Element[]): ImagesElements => {
  return buttons.map((button, index) => {
    button.innerHTML = ''

    const imageTag = document.createElement('img')
    const imageSrc = nth(imagesSources, index)

    if (isNil(imageSrc)) {
      return null
    }

    imageTag.src = imageSrc
    button.appendChild(imageTag)

    return imageTag
  })
}

export const updateImages = (newImagesSources: string[], images: ImagesElements): void => {
  images.forEach((image, i) => {
    const source = newImagesSources[i]

    if (!isNil(image) && !isNil(newImagesSources)) {
      image.src = source
    }
  })
}
