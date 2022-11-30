import { isNil } from 'lodash'
import { TabConfig } from '../config'
import { withPrefix } from '../utils/str'
import { Nullable } from '../utils/types'
import { TabElements } from './elements'
import { getImageNameFromPath, toLocalImagePath } from './images'

export const makeShowLoading = (config: TabConfig, element: Nullable<HTMLElement>) => () => {
  if (isNil(element)) {
    return
  }

  const loadingTag = document.createElement('div')
  loadingTag.classList.add(withPrefix(config.css.classPrefix, config.css.classesSuffixes.spinner))

  element.after(loadingTag)
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
  }
}

const turnToTabBrowsing = (config: TabConfig, elements: TabElements): void => {
  const imageBrowsingClassName = withPrefix(config.css.classPrefix, config.css.classesSuffixes.imageSelectedMode)

  elements.gallery.gallery.classList.remove(imageBrowsingClassName)
  elements.gallery.container.classList.remove(imageBrowsingClassName)

  const imagePreview = elements.gallery.gallery.previousElementSibling
  imagePreview?.remove()
}

export const makeUpdateGalleryModes = (config: TabConfig, elements: TabElements) => (selectedImageSrc: Nullable<string>) => {
  if (isNil(selectedImageSrc)) {
    turnToTabBrowsing(config, elements)
  } else {
    turnToImageBrowsing(config, elements, selectedImageSrc)
  }
}

export const makeUpdateSelection = (config: TabConfig, elements: TabElements) => (selectedImageSrc: Nullable<string>) => {
  const selectedClassName = withPrefix(config.css.classPrefix, config.css.classesSuffixes.selectedImageButton)
  const selectedImageName = !isNil(selectedImageSrc) ? getImageNameFromPath(selectedImageSrc) : null

  elements.buttons.images.forEach((imageButton) => imageButton.classList.remove(selectedClassName))
  if (!isNil(selectedImageName)) {
    const selectedButton = elements.buttons.images.find((buttonEl) => {
      const src = buttonEl.querySelector('img')?.src
      return !isNil(src) && decodeURIComponent(src).includes(selectedImageName)
    })

    console.log({ selectedButton })

    selectedButton?.classList.add(selectedClassName)
  }
}
