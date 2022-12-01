import { isNil } from 'lodash'
import { BaseTabConfig, StaticConfig, TabConfig } from '../config'
import { createEmptyContainer } from './elements'
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

type MakeExpandConfigArg = Readonly<{
  staticConfig: StaticConfig
  preloadRoot: Element
  appRoot: Nullable<ShadowRoot>
}>

export const makeExpandConfig = ({ staticConfig, appRoot, preloadRoot }: MakeExpandConfigArg) => (tabRoot: HTMLElement): Nullable<BaseTabConfig> => {
  const tabId = extractTabId(staticConfig, tabRoot)
  const gradioContainer = appRoot?.querySelector(staticConfig.gradio.containerCSSClass)

  if (isNil(tabId) || isNil(appRoot) || isNil(gradioContainer)) {
    return null
  }

  const bigPictureRoot = createEmptyContainer(appRoot)

  return {
    staticConfig,
    runtimeConfig: {
      bigPictureRoot,
      appRoot,
      tabRoot,
      tabId,
      preloadRoot,
      gradioContainer
    }
  }
}

export const includeOtherTabConfigs = (thisTab: BaseTabConfig, _: number, allTabs: BaseTabConfig[]): TabConfig => {
  const allExpectThis = allTabs.filter((tab) => tab.runtimeConfig.tabId !== thisTab.runtimeConfig.tabId)

  return {
    ...thisTab,
    otherTabs: allExpectThis
  }
}
