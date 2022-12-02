import { isNil, isString, noop } from 'lodash'

import { eq } from './fn'
import { isArrayOf, isObjectWithKeys } from './guards'
import { toLowerCase } from './str'
import { Nullable } from './types'

export enum Keys {
  ArrowRight = 'ArrowRight',
  ArrowLeft = 'ArrowLeft',
  ArrowUp = 'ArrowUp',
  ArrowDown = 'ArrowDown',
  Esc = 'Escape'
}

type KeyboardEventListener = (e: KeyboardEvent) => void
type KeyboardEventCallback = () => void
type OnKeyConfig = Readonly<{ shift: boolean }>

export function onKey (selectedKey: string | string[], callback: KeyboardEventCallback): KeyboardEventListener
export function onKey (selectedKey: string | string[], config: OnKeyConfig, callback: KeyboardEventCallback): KeyboardEventListener
export function onKey (selectedKey: string | string[], configOrCallback: KeyboardEventCallback | OnKeyConfig, callback?: KeyboardEventCallback): KeyboardEventListener {
  const cb = callback ?? (isObjectWithKeys<OnKeyConfig>(configOrCallback, ['shift']) ? noop : configOrCallback)
  const config: Nullable<OnKeyConfig> = isObjectWithKeys<OnKeyConfig>(configOrCallback, ['shift']) ? configOrCallback : null

  return (e: KeyboardEvent) => {
    const keys = (isArrayOf(selectedKey, isString) ? selectedKey : [selectedKey]).map(toLowerCase)
    const parsedPressedKey = toLowerCase(e.key)

    if (!keys.some(eq(parsedPressedKey))) {
      return
    }

    if (!isNil(config) && config.shift !== e.shiftKey) {
      return
    }

    e.preventDefault()
    cb()
  }
}
