const staticConfig = {
  gradioAppTag: 'gradio-app',
  gradioHiddenElementCSSClass: '!hidden',
  extensionId: 'images_gallery',
  css: {
    classPrefix: 'image_gallery',
    classesSuffixes: {
      spinner: 'spinner',
      imageSelectedMode: 'imageSelectedMode',
      selectedImage: 'selectedImage',
      selectedImageButton: 'selectedImageButton'
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
    selectedImagePath: 'selectedImagePath'
  }
} as const

export type RuntimeConfig = Readonly<{
  tabId: string
  appRoot: ShadowRoot
  tabRoot: Element
  preloadRoot: Element
}>

export type BaseTabConfig = StaticConfig & RuntimeConfig
export type StaticConfig = typeof staticConfig

export type TabConfig = BaseTabConfig & Readonly<{
  otherTabs: BaseTabConfig[]
}>

export default staticConfig
