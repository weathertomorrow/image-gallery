import { TabConfig } from '../config'
import { withPrefix } from './str'

export const createEmptyContainer = (root: Element | ShadowRoot): HTMLElement => {
  const container = document.createElement('div')
  root.appendChild(container)

  return container
}

export const generateClassName = (config: TabConfig, element: keyof TabConfig['staticConfig']['css']['classesSuffixes']): string => {
  return withPrefix(config.staticConfig.css.classPrefix, config.staticConfig.css.classesSuffixes[element])
}
