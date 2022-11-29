import { isNil } from 'lodash'
import { TabConfig } from '../config'
import { withPrefix } from '../utils/str'
import { Nullable } from '../utils/types'

export const makeShowLoading = (config: TabConfig, element: Nullable<HTMLElement>) => () => {
  if (isNil(element)) {
    return
  }

  const loadingTag = document.createElement('div')
  loadingTag.classList.add(withPrefix(config.cssClassPrefix, config.suffixes.spinner))

  element.after(loadingTag)
}
