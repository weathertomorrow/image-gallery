import { debounce, isNil } from 'lodash'
import { TabConfig } from '../config'
import { withPrefix } from '../utils/str'
import { Nullable } from '../utils/types'
import { getFirstImageInTab, getLastImageInTab, TabElements } from './elements'
import { emitClick } from './eventEmitters'
import { extractImageSrcs, getImageNameFromPath, ImagesElements, toLocalImagePath, UpdateImages } from './images'
import { SelectedImageCallback, ImageSourcesCallback } from './listeners'
import { getSelectedImagePath } from './utils'

export const makeShowLoading = (config: TabConfig, element: Nullable<HTMLElement>) => () => {
  if (isNil(element)) {
    return
  }

  const loadingTag = document.createElement('div')
  loadingTag.classList.add(withPrefix(config.css.classPrefix, config.css.classesSuffixes.spinner))

  element.after(loadingTag)
}

const scrollToElement = (element: Nullable<Element>): void => {
  element?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
}

const findButtonForImage = (elements: TabElements, image: Nullable<string>): Nullable<HTMLElement> => {
  if (isNil(image)) {
    return null
  }

  const selectedImageName = getImageNameFromPath(image)

  if (isNil(selectedImageName)) {
    return null
  }

  return elements.buttons.images.find((buttonEl) => {
    const src = buttonEl.querySelector('img')?.src
    return !isNil(src) && decodeURIComponent(src).includes(selectedImageName)
  })
}

const turnToImageBrowsing = (config: TabConfig, elements: TabElements, selectedImageSrc: string): void => {
  const imageBrowsingClassName = withPrefix(config.css.classPrefix, config.css.classesSuffixes.imageSelectedMode)

  elements.gallery.gallery.classList.add(imageBrowsingClassName)
  elements.gallery.container.classList.add(imageBrowsingClassName)

  const prevSibling = elements.gallery.gallery.previousElementSibling

  if (!isNil(prevSibling) && prevSibling instanceof HTMLImageElement) {
    prevSibling.src = toLocalImagePath(selectedImageSrc)
  } else {
    const imagePreview = document.createElement('img')
    imagePreview.src = toLocalImagePath(selectedImageSrc)
    imagePreview.classList.add(withPrefix(config.css.classPrefix, config.css.classesSuffixes.selectedImage))
    elements.gallery.gallery.before(imagePreview)

    scrollToElement(findButtonForImage(elements, selectedImageSrc))
  }
}

const turnToTabBrowsing = (config: TabConfig, elements: TabElements): void => {
  const imageBrowsingClassName = withPrefix(config.css.classPrefix, config.css.classesSuffixes.imageSelectedMode)

  elements.gallery.gallery.classList.remove(imageBrowsingClassName)
  elements.gallery.container.classList.remove(imageBrowsingClassName)

  const imagePreview = elements.gallery.gallery.previousElementSibling
  imagePreview?.remove()
}

export const makeUpdateGalleryModes = (config: TabConfig, elements: TabElements): SelectedImageCallback => (selectedImageSrc: Nullable<string>) => {
  if (isNil(selectedImageSrc)) {
    turnToTabBrowsing(config, elements)
  } else {
    turnToImageBrowsing(config, elements, selectedImageSrc)
  }
}

type MakeUpdateSelectionReturnValue = Readonly<{
  onImageChange: SelectedImageCallback
  onPageChange: () => void
}>

export const makeUpdateSelection = (config: TabConfig, elements: TabElements): MakeUpdateSelectionReturnValue => {
  let previouslySelectedImage: Nullable<string> = null

  const onImageChange: SelectedImageCallback = (selectedImageSrc) => {
    const selectedClassName = withPrefix(config.css.classPrefix, config.css.classesSuffixes.selectedImageButton)
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
  }, config.debounceMs)
}

export const makeClickSiblingToSelectedImage = (type: 'previous' | 'next', elements: TabElements) => () => {
  const currentlySelected = findButtonForImage(elements, getSelectedImagePath(elements.imageSrcs.selected))
  const sibling = currentlySelected?.[type === 'next' ? 'nextElementSibling' : 'previousElementSibling']

  if (!isNil(sibling) && sibling instanceof HTMLElement) {
    emitClick(sibling)
    scrollToElement(sibling)
  } else if (isNil(sibling)) {
    if (type === 'next') {
      const firstImage = getFirstImageInTab(elements)
      emitClick(firstImage)
      scrollToElement(firstImage)
    } else {
      const lastImage = getLastImageInTab(elements)
      emitClick(lastImage)
      scrollToElement(lastImage)
    }
  }
}
