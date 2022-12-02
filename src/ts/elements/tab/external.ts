import { ConfigWithOtherTabs } from '../../config'

import { isNotNil } from '../../utils/guards'
import { withPrefix } from '../../utils/str'
import { Nullable } from '../../utils/types'
import { extensionElementById } from '../utils'

export type ExternalElements = Readonly<{
  moveToThisTabButtons: HTMLButtonElement[]
}>

export const getMoveToThisTabButtons = (config: ConfigWithOtherTabs): HTMLButtonElement[] => {
  return config.otherTabs
    .map((otherTab) => {
      const query = extensionElementById(config.staticConfig, 'moveToButton', withPrefix(otherTab.runtimeConfig.tabId, config.runtimeConfig.tabId))
      return config.runtimeConfig.appRoot.querySelector<HTMLButtonElement>(query)
    })
    .filter(isNotNil)
}

export const getExternalElements = (config: ConfigWithOtherTabs): Nullable<ExternalElements> => {
  const buttons = getMoveToThisTabButtons(config)

  return {
    moveToThisTabButtons: buttons
  }
}
