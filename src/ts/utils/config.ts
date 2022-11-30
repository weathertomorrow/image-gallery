import { isNil } from 'lodash'
import { BaseTabConfig, StaticConfig, TabConfig } from '../config'
import { isEmpty } from './guards'
import { withSuffix } from './str'
import { Nullable } from './types'

const extractTabId = (staticConfig: StaticConfig, tab: Element): Nullable<string> => {
  const id = tab.id.replace(withSuffix(staticConfig.extensionId, staticConfig.suffixes.galleryTab), '')
    .replace(/_$/, '')

  if (!isEmpty(id)) {
    return id
  }

  return null
}

export const makeExpandConfig = (staticConfig: StaticConfig, preloadRoot: Element, appRoot: Nullable<ShadowRoot>) => (tabRoot: HTMLElement): Nullable<BaseTabConfig> => {
  const tabId = extractTabId(staticConfig, tabRoot)

  if (isNil(tabId) || isNil(appRoot)) {
    return null
  }

  return { ...staticConfig, appRoot, tabRoot, tabId, preloadRoot }
}

export const includeOtherTabConfigs = (thisTab: BaseTabConfig, _: number, allTabs: BaseTabConfig[]): TabConfig => {
  const allExpectThis = allTabs.filter((tab) => tab.tabId !== thisTab.tabId)

  return {
    ...thisTab,
    otherTabs: allExpectThis
  }
}
