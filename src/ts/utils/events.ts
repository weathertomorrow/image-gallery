import { isString } from 'lodash'

import { eq } from './fn'
import { isArrayOf } from './guards'
import { toLowerCase } from './str'

export enum Keys {
  ArrowRight = 'ArrowRight',
  ArrowLeft = 'ArrowLeft',
  ArrowUp = 'ArrowUp',
  ArrowDown = 'ArrowDown',
  Esc = 'Escape'
}

export const onKey = (selectedKey: string | string[], callback: () => void) => (e: KeyboardEvent) => {
  const keys = (isArrayOf(selectedKey, isString) ? selectedKey : [selectedKey]).map(toLowerCase)
  const parsedPressedKey = toLowerCase(e.key)

  if (keys.some(eq(parsedPressedKey))) {
    e.preventDefault()
    callback()
  }
}
