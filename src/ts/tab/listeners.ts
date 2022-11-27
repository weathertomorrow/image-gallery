import { isNil } from 'lodash'
import { isEmpty } from './guards'

export const makeImageSourcesObserver = (callback: (node: Element) => void): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation
  console.log(mutation)

  if (!isNil(target) && target instanceof Element) {
    callback(target)
  }
}

type MakeImagesLoadListenerArg = Readonly<{
  imagesPerPage: number
  onDone: () => void
  onReset: () => void
}>

type MakeImagesLoadListenerReturnValue = Readonly<{
  reset: () => void
  listen: () => void
}>

export const makeImageLoadListener = ({
  imagesPerPage,
  onDone,
  onReset
}: MakeImagesLoadListenerArg): MakeImagesLoadListenerReturnValue => {
  let progress = imagesPerPage

  return {
    reset: () => {
      onReset()
      progress = imagesPerPage
    },
    listen: () => {
      progress = Math.max(0, progress - 1)
      console.log({ progress })
      if (progress === 0) {
        onDone()
      }
    }
  }
}
