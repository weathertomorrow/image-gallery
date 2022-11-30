import { Nullable } from '../utils/types'

export const emitClick = (element: Nullable<HTMLElement>): void => {
  element?.click()
}

export const makeEmitClick = (element: Nullable<HTMLElement>) => () => emitClick(element)
