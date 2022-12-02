import { debounce, defer, first, isNil, last } from 'lodash'

import { TabConfig } from '../../config/types'
import { TabElements } from '../../elements/tab'

import { scrollToElement } from '../../utils/dom'
import { call } from '../../utils/fn'
import { withPrefix } from '../../utils/str'
import { Nullable } from '../../utils/types'
import { emitClick, emitFocus } from '../events/emitters'
import { SelectedImageCallback, ImageSourcesCallback } from '../events/listeners'
import { findButtonForImage, getSelectedImagePath, toLocalImagePath } from '../utils'

import { extractImageSrcs, ImagesElements, UpdateImages } from './images'

const generateClassName = (config: TabConfig, element: keyof TabConfig['staticConfig']['css']['classesSuffixes']): string => {
  return withPrefix(config.staticConfig.css.classPrefix, config.staticConfig.css.classesSuffixes[element])
}

export const makeShowLoading = (config: TabConfig, element: Nullable<HTMLElement>) => () => {
  if (isNil(element)) {
    return
  }

  const loadingTag = document.createElement('div')
  loadingTag.classList.add(generateClassName(config, 'spinner'))

  element.after(loadingTag)
}

const createImagePreviewNode = (config: TabConfig, elements: TabElements, selectedImageSrc: string): HTMLImageElement => {
  const imagePreview = document.createElement('img')
  imagePreview.src = toLocalImagePath(selectedImageSrc)
  imagePreview.classList.add(generateClassName(config, 'selectedImage'))

  elements.gallery.gallery.before(imagePreview)

  return imagePreview
}

type OnImageCreatedCallback = (image: HTMLImageElement) => void

const turnToImageBrowsing = (config: TabConfig, elements: TabElements, selectedImageSrc: string, onImageCreated: OnImageCreatedCallback): void => {
  const imageBrowsingClassName = generateClassName(config, 'imageSelectedMode')
  const existingSelectedImageNode = elements.MUTABLE.selectedImage

  elements.gallery.gallery.classList.add(imageBrowsingClassName)
  elements.gallery.container.classList.add(imageBrowsingClassName)

  if (!isNil(existingSelectedImageNode)) {
    existingSelectedImageNode.src = toLocalImagePath(selectedImageSrc)
  } else {
    elements.MUTABLE.selectedImage = createImagePreviewNode(config, elements, selectedImageSrc)
    onImageCreated(elements.MUTABLE.selectedImage)

    scrollToElement(findButtonForImage(elements, selectedImageSrc))
    defer(() => scrollToElement(elements.gallery.container, false))
  }
}

const turnToTabBrowsing = (config: TabConfig, elements: TabElements): void => {
  const imageBrowsingClassName = generateClassName(config, 'imageSelectedMode')

  elements.gallery.gallery.classList.remove(imageBrowsingClassName)
  elements.gallery.container.classList.remove(imageBrowsingClassName)

  elements.MUTABLE.selectedImage?.remove()
  elements.MUTABLE.selectedImage = null
}

export const makeUpdateGalleryModes = (config: TabConfig, elements: TabElements, onImageCreated: OnImageCreatedCallback): SelectedImageCallback => (selectedImageSrc: Nullable<string>) => {
  if (isNil(selectedImageSrc)) {
    turnToTabBrowsing(config, elements)
  } else {
    turnToImageBrowsing(config, elements, selectedImageSrc, onImageCreated)
  }
}

type MakeUpdateSelectionReturnValue = Readonly<{
  onImageChange: SelectedImageCallback
  onPageChange: () => void
}>

export const makeUpdateSelection = (config: TabConfig, elements: TabElements): MakeUpdateSelectionReturnValue => {
  let previouslySelectedImage: Nullable<string> = null

  const onImageChange: SelectedImageCallback = (selectedImageSrc) => {
    const selectedClassName = generateClassName(config, 'selectedImageButton')
    elements.buttons.images.forEach((imageButton) => imageButton.classList.remove(selectedClassName))

    if (!isNil(selectedImageSrc)) {
      const selectedButton = findButtonForImage(elements, selectedImageSrc)
      selectedButton?.classList.add(selectedClassName)
    }
  }

  const onPageChange = (): void => onImageChange(previouslySelectedImage)

  return {
    onPageChange,
    onImageChange: (selectedImageSrc) => {
      onImageChange(selectedImageSrc)
      previouslySelectedImage = selectedImageSrc
    }
  }
}

export const makeOnMainPageSourcesChanged = (
  config: TabConfig,
  images: ImagesElements,
  resetLoading: () => void,
  updateImages: UpdateImages
): ImageSourcesCallback => {
  return debounce<ImageSourcesCallback>(async (element) => {
    resetLoading()
    void updateImages(extractImageSrcs(element), images)
  }, config.staticConfig.debounceMs)
}

export const makeClickSiblingToSelectedImage = (type: 'previous' | 'next', elements: TabElements) => () => {
  const currentlySelected = findButtonForImage(elements, getSelectedImagePath(elements.imageSrcs.selected))
  const sibling = currentlySelected?.[type === 'next' ? 'nextElementSibling' : 'previousElementSibling']

  const events = [emitClick, emitFocus]

  if (!isNil(sibling) && sibling instanceof HTMLElement) {
    events.forEach(call(sibling))
    scrollToElement(sibling)
  } else if (isNil(sibling)) {
    if (type === 'next') {
      const firstImage = first(elements.buttons.images)
      events.forEach(call(firstImage))
      scrollToElement(firstImage)
    } else {
      const lastImage = last(elements.buttons.images)
      events.forEach(call(lastImage))
      scrollToElement(lastImage)
    }
  }
}

type BigPictureModeHandlers = Readonly<{
  close: () => void
  update: SelectedImageCallback
  open: () => void
}>

export const makeBigPictureModeHandlers = (config: TabConfig, elements: TabElements): BigPictureModeHandlers => {
  const bigPictureModeClassName = generateClassName(config, 'bigPictureMode')

  const close = (): void => {
    config.runtimeConfig.bigPictureRoot.classList.remove(bigPictureModeClassName)
    config.runtimeConfig.gradioContainer.classList.remove(bigPictureModeClassName)

    config.runtimeConfig.bigPictureRoot.innerHTML = ''
    elements.MUTABLE.bigPictureImage = null
  }

  return {
    close,
    update: (image) => {
      if (isNil(image)) {
        return close()
      }

      const imageEl = elements.MUTABLE?.bigPictureImage

      if (isNil(imageEl)) {
        return close()
      }

      imageEl.src = toLocalImagePath(image)
    },
    open: () => {
      const selectedPicture = elements.MUTABLE.selectedImage

      if (isNil(selectedPicture)) {
        return
      }

      if (isNil(elements.MUTABLE.bigPictureImage)) {
        const bigPictureImageNode = document.createElement('img')
        config.runtimeConfig.bigPictureRoot.appendChild(bigPictureImageNode)
        elements.MUTABLE.bigPictureImage = bigPictureImageNode
      }

      elements.MUTABLE.bigPictureImage.src = selectedPicture.src
      config.runtimeConfig.bigPictureRoot.classList.add(generateClassName(config, 'bigPictureModeContainer'))
      config.runtimeConfig.bigPictureRoot.classList.add(bigPictureModeClassName)
      config.runtimeConfig.gradioContainer.classList.add(bigPictureModeClassName)
    }
  }
}
