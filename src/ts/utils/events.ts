import { isString } from 'lodash'
import { isArrayOf } from './guards'

export enum Keys {
  ArrowRight = 'ArrowRight',
  ArrowLeft = 'ArrowLeft',
  ArrowUp = 'ArrowUp',
  ArrowDown = 'ArrowDown',
  Esc = 'Escape'
}

export const onKey = (selectedKey: string | string[], callback: () => void) => (e: KeyboardEvent) => {
  const keys = isArrayOf(selectedKey, isString) ? selectedKey : [selectedKey]

  if (keys.some((key) => key === e.key)) {
    e.preventDefault()
    callback()
  }
}
