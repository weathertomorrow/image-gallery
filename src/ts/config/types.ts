import { TabElements } from '../elements/tab'
import { ExternalElements } from '../elements/tab/external'
import { Nullable } from '../utils/types'

import { staticConfig } from './staticConfig'

import { ConfigWithTabInfo } from '.'

export type StaticConfig = typeof staticConfig

export type RuntimeConfig = Readonly<{
  tabId: string
  extensionRoot: Element
  appRoot: ShadowRoot
  tabRoot: HTMLElement
  preloadRoot: Element
  bigPictureRoot: Element
  gradioContainer: Element
}>

export type BaseTabConfig = Readonly<{
  staticConfig: StaticConfig
  runtimeConfig: RuntimeConfig
}>

export type TabInfo = Readonly<{
  keybind: Nullable<string>
}>

export type TabConfig = BaseTabConfig & Readonly<{
  otherTabs: ConfigWithTabInfo[]
  externalElements: ExternalElements
  tabElements: TabElements
  tabInfo: TabInfo
  index: number
}>

export default staticConfig
