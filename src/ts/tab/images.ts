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

export const makeChangeImagesVisiblity = (shouldBeVisible: boolean, images: ImagesElements) => () => {
  images.forEach((image) => {
    if (!isNil(image)) {
      image.style.opacity = shouldBeVisible ? '1' : '0'
    }
  })
}

export type MakeUpdateImagesReturnValue = Readonly<{
  shouldCancel: { current: boolean }
  updateImages: (newImagesSources: string[], images: ImagesElements) => Promise<boolean>
}>

export const makeUpdateImages = (listener: (imageIndex: number) => void): MakeUpdateImagesReturnValue => {
  const shouldCancel = { current: false }

  return {
    shouldCancel,
    updateImages: async (newImagesSources, images) => {
      // for loop instead of a foreach so that it can be cancelled early when user is changing pages quickly
      for (let i = 0; i < images.length; i++) {
        if (shouldCancel.current) return false

        const image = images[i]
        const source = newImagesSources[i]

        if (!isNil(image) && !isNil(newImagesSources)) {
          image.src = source

          image.onload = () => listener(i)
        }
      }

      return true
    }
  }
}
