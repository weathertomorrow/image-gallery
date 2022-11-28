import { isNil } from 'lodash'
import { isEmpty } from './guards'

export const makeImageSourcesListener = (callback: (node: Element) => void): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation

  if (!isNil(target) && target instanceof Element) {
    callback(target)
  }
}

export const makeProgressBarListener = (isDone: (done: boolean) => void): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation

  if (!isNil(target) && target instanceof Element && isEmpty(Array.from(target.children))) {
    isDone(true)
  } else {
    isDone(false)
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
      if (progress === 0) {
        onDone()
      }
    }
  }
}

export const makeHTMLEventListener = (listener: () => void, eventType: keyof HTMLElementEventMap = 'click') => (element: HTMLElement) => {
  element.addEventListener(eventType, listener)
}
