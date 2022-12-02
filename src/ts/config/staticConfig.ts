export const staticConfig = {
  gradio: {
    appTag: 'gradio-app',
    hiddenElementCSSClass: '!hidden',
    containerCSSClass: '.gradio-container'
  },
  extensionId: 'images_gallery',
  css: {
    classPrefix: 'image_gallery',
    classesSuffixes: {
      spinner: 'spinner',
      imageSelectedMode: 'imageSelectedMode',
      selectedImage: 'selectedImage',
      selectedImageButton: 'selectedImageButton',
      bigPictureMode: 'bigPictureMode',
      bigPictureModeContainer: 'bigPictureModeContainer'
    }
  },
  debounceMs: 200,
  suffixes: {
    extensionTab: 'extensionTab',
    galleryTab: 'galleryTab',
    gallery: 'gallery',
    galleryContainer: 'galleryContainer',
    imgSrcs: 'imgSrcs',
    imgButton: 'imgButton',
    moveToButton: 'moveToButton',
    refreshButton: 'refreshButton',
    progressBar: 'progressbar',
    generateThumbnailsButton: 'generateThumbnailsButton',
    generateThumbnailsContainer: 'generateThumbnailsContainer',
    selectedImagePath: 'selectedImagePath',
    navigationControllsContainer: 'navigationControllsContainer',
    hiddenPageIndex: 'hiddenPageIndex',
    hiddenTabInfo: 'hiddenTabInfo',
    deselectImageButton: 'deselectImageButton'
  }
} as const
