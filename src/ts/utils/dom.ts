import { Nullable } from '../utils/types'

export const createEmptyContainer = (root: Element | ShadowRoot): HTMLElement => {
  const container = document.createElement('div')
  root.appendChild(container)

  return container
}

export const scrollToElement = (element: Nullable<Element>, nearest = true): void => {
  element?.scrollIntoView({ behavior: 'smooth', block: nearest ? 'nearest' : undefined })
}

export const makeScrollToElement = (element: Nullable<Element>, nearest?: boolean) => () => {
  return scrollToElement(element, nearest)
}

export const contains = (el: HTMLElement) => (parent: HTMLElement) => parent.contains(el)
