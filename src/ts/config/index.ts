import { isNil } from 'lodash'

import { getElements } from '../elements/tab'
import { getExternalElements } from '../elements/tab/external'
import { createEmptyContainer } from '../utils/dom'
import { isEmpty, isNotNil, isObjectWithKeys } from '../utils/guards'
import { withSuffix } from '../utils/str'
import { Nullable } from '../utils/types'

import { BaseTabConfig, RuntimeConfig, StaticConfig, TabConfig, TabInfo } from './types'

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

type ConfigWithElements = BaseTabConfig & Pick<TabConfig, 'tabElements'>
export const makeGetConfigWithElements = ({ staticConfig, appRoot, preloadRoot }: MakeExpandConfigArg) => (tabRoot: HTMLElement): Nullable<ConfigWithElements> => {
  const tabId = extractTabId(staticConfig, tabRoot)
  const gradioContainer = appRoot?.querySelector(staticConfig.gradio.containerCSSClass)

  if (isNil(tabId) || isNil(appRoot) || isNil(gradioContainer)) {
    return null
  }

  const bigPictureRoot = createEmptyContainer(appRoot)
  const runtimeConfig: RuntimeConfig = {
    bigPictureRoot,
    appRoot,
    tabRoot,
    tabId,
    preloadRoot,
    gradioContainer
  }

  const tabElements = getElements({ runtimeConfig, staticConfig })

  if (isNil(tabElements)) {
    return null
  }

  return {
    staticConfig,
    runtimeConfig,
    tabElements
  }
}

export type ConfigWithTabInfo = ConfigWithElements & Pick<TabConfig, 'tabInfo'>
export const getConfigWithTabInfo = (configWithElements: Nullable<ConfigWithElements>): Nullable<ConfigWithTabInfo> => {
  if (isNil(configWithElements)) {
    return null
  }

  const tabInfo = JSON.parse(configWithElements?.tabElements?.tabInfo.innerHTML ?? 'null')

  if (isObjectWithKeys<TabInfo>(tabInfo, ['keybind'])) {
    return {
      ...configWithElements,
      tabInfo
    }
  }

  return null
}

export type ConfigWithOtherTabs = ConfigWithTabInfo & Pick<TabConfig, 'otherTabs'>
export const getConfigWithOtherTabs = (thisTab: Nullable<ConfigWithTabInfo>, _: number, allTabs: Array<Nullable<ConfigWithTabInfo>>): Nullable<ConfigWithOtherTabs> => {
  if (isNil(thisTab)) {
    return null
  }

  const allExpectThis = allTabs.filter((tab) => tab?.runtimeConfig.tabId !== thisTab.runtimeConfig.tabId)
    .filter(isNotNil)

  return {
    ...thisTab,
    otherTabs: allExpectThis
  }
}

export type ConfigWithExternalElements = ConfigWithOtherTabs & Pick<TabConfig, 'externalElements'>
export const getConfigWithExternalElements = (configWithTabInfo: Nullable<ConfigWithOtherTabs>): Nullable<ConfigWithExternalElements> => {
  if (isNil(configWithTabInfo)) {
    return null
  }

  const externalElements = getExternalElements(configWithTabInfo)

  if (isNil(externalElements)) {
    return null
  }

  return {
    ...configWithTabInfo,
    externalElements
  }
}
