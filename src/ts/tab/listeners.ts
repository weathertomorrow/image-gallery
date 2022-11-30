import { isNil } from 'lodash'
import { TabConfig } from '../config'
import { Nullable } from '../utils/types'
import { isEmpty } from './guards'

export type ImageSourcesCallback = (node: Element) => void
export const makeImageSourcesListener = (callback: ImageSourcesCallback): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation

  if (!isNil(target) && target instanceof Element) {
    callback(target)
  }
}

export type DoneCallback = (done: boolean) => void
export const makeProgressBarListener = (isDone: DoneCallback): MutationCallback => (mutation) => {
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

export const makeGenerateThumbnailsListener = (config: TabConfig, isDone: DoneCallback): MutationCallback => (mutation) => {
  if (isEmpty(mutation)) {
    return
  }

  const [{ target }] = mutation

  if (!isNil(target) && target instanceof Element && target.classList.contains(config.gradioHiddenElementCSSClass)) {
    isDone(true)
  } else {
    isDone(false)
  }
}

export type SelectedImageCallback = (path: Nullable<string>) => void
export const makeSelectedImageListener = (onChange: SelectedImageCallback): MutationCallback => {
  let prevValue: Nullable<string> = null

  return (mutation) => {
    if (isEmpty(mutation)) {
      return
    }

    const [{ target }] = mutation

    if (!isNil(target) && target instanceof HTMLTextAreaElement) {
      const parsedValue = isEmpty(target.value) ? null : target.value

      if (prevValue !== parsedValue) {
        onChange(parsedValue)
      }

      prevValue = parsedValue
    }
  }
}

export type PageChangeCallback = (page: number) => void
export const makePageChangeListener = (onChange: PageChangeCallback): MutationCallback => {
  let prevValue = 0

  return (mutation) => {
    if (isEmpty(mutation)) {
      return
    }

    const [{ target }] = mutation

    if (!isNil(target) && target instanceof Element) {
      const pageIndex = Number(target.innerHTML)

      if (Number.isFinite(pageIndex)) {
        if (pageIndex !== prevValue) {
          onChange(pageIndex)
        }

        prevValue = pageIndex
      }
    }
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
