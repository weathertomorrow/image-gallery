import { StaticConfig } from '../config'
import { isEmpty } from './guards'

export const withSuffix = (sufix: string, name: string): string => {
  return `${name}_${sufix}`
}

export const withPrefix = (prefix: string, name: string): string => withSuffix(name, prefix)

export const tabElementQueryString = (config: StaticConfig, element: keyof StaticConfig['suffixes'], prefix = ''): string => {
  const id = withSuffix(config.extensionId, config.suffixes[element])
  return `[id*=${isEmpty(prefix) ? id : withPrefix(prefix, id)}]`
}
