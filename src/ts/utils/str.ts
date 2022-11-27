import { Config } from '../config'

export const withSuffix = (sufix: string, name: string): string => {
  return `${name}_${sufix}`
}

export const tabElementQueryString = (config: Config, element: keyof Config['suffixes']): string => {
  return `[id*=${withSuffix(config.extensionId, config.suffixes[element])}]`
}
