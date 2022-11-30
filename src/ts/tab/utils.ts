import { TabConfig } from '../config'
import { isEmpty } from '../utils/guards'
import { Nullable } from '../utils/types'

export const ifTabActive = <T, U>(tab: TabConfig, fn: (arg: T) => U) => {
  return (arg: T) => {
    if (tab.tabRoot.style.display !== 'none') {
      return fn(arg)
    }
    return null
  }
}

export const getSelectedImagePath = (target: HTMLTextAreaElement): Nullable<string> => {
  const parsedValue = isEmpty(target.value) ? null : target.value
  return parsedValue
}
