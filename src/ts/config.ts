const config = {
  gradioAppTag: 'gradio-app',
  extensionId: 'images_gallery',
  cssClassPrefix: 'image_gallery',
  suffixes: {
    extensionTab: 'extensionTab',
    galleryTab: 'galleryTab',
    gallery: 'gallery',
    imgSrcs: 'imgSrcs',
    imgButton: 'imgButton'
  }
} as const

export type Config = typeof config

export default config
