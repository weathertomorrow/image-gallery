import { StaticConfig } from '../config/types'
import { isEmpty } from '../utils/guards'
import { withPrefix, withSuffix } from '../utils/str'
import { Nullable } from '../utils/types'

export const extensionElementById = (config: StaticConfig, element: keyof StaticConfig['suffixes'], prefix = ''): string => {
  const id = withSuffix(config.extensionId, config.suffixes[element])
  return `[id*=${isEmpty(prefix) ? id : withPrefix(prefix, id)}]`
}

export const extractTabId = (staticConfig: StaticConfig, possibleId: string): Nullable<string> => {
  const id = possibleId.replace(withSuffix(staticConfig.extensionId, staticConfig.suffixes.galleryTab), '')
    .trim()
    .toLowerCase()
    .replace(/_$/, '')

  if (!isEmpty(id)) {
    return id
  }

  return null
}

export const makeExtractTabId = (staticConfig: StaticConfig) => (possibleId: string) => extractTabId(staticConfig, possibleId)
