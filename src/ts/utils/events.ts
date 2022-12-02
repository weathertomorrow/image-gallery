import { isNil, isString, noop } from 'lodash'

import { eq } from './fn'
import { isNotNil, isObjectWithKeys } from './guards'
import { toLowerCase } from './str'
import { Nullable } from './types'

export enum Keys {
  ArrowRight = 'ArrowRight',
  ArrowLeft = 'ArrowLeft',
  ArrowUp = 'ArrowUp',
  ArrowDown = 'ArrowDown',
  Esc = 'Escape'
}

const numToShiftKeyBind = Object.fromEntries([
  ['1', '!'],
  ['2', '@'],
  ['3', '#'],
  ['4', '$'],
  ['5', '%'],
  ['6', '^'],
  ['7', '&'],
  ['8', '*'],
  ['9', '('],
  ['10', ')']
])

const parseKeybind = (keybind: string): string => {
  const inLowerCase = toLowerCase(keybind)

  if (inLowerCase in numToShiftKeyBind) {
    return numToShiftKeyBind[inLowerCase]
  }

  return inLowerCase
}

type KeyboardEventListener = (e: KeyboardEvent) => void
type KeyboardEventCallback = () => void
type OnKeyConfig = Readonly<{ shift: boolean }>

export function onKey (selectedKey: Nullable<string> | Array<Nullable<string>>, callback: KeyboardEventCallback): KeyboardEventListener
export function onKey (selectedKey: Nullable<string> | Array<Nullable<string>>, config: OnKeyConfig, callback: KeyboardEventCallback): KeyboardEventListener
export function onKey (selectedKey: Nullable<string> | Array<Nullable<string>>, configOrCallback: KeyboardEventCallback | OnKeyConfig, callback?: KeyboardEventCallback): KeyboardEventListener {
  if (isNil(selectedKey)) {
    return noop
  }

  const cb = callback ?? (isObjectWithKeys<OnKeyConfig>(configOrCallback, ['shift']) ? noop : configOrCallback)
  const config: Nullable<OnKeyConfig> = isObjectWithKeys<OnKeyConfig>(configOrCallback, ['shift']) ? configOrCallback : null

  const keys = (isString(selectedKey) || isNil(selectedKey) ? [selectedKey] : selectedKey)
    .filter(isNotNil)
    .map(parseKeybind)

  return (e: KeyboardEvent) => {
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
