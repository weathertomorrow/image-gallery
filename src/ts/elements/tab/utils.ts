import { StaticConfig } from '../../config/types'

import { isEmpty } from '../../utils/guards'
import { withPrefix, withSuffix } from '../../utils/str'

export const tabElementQueryString = (config: StaticConfig, element: keyof StaticConfig['suffixes'], prefix = ''): string => {
  const id = withSuffix(config.extensionId, config.suffixes[element])
  return `[id*=${isEmpty(prefix) ? id : withPrefix(prefix, id)}]`
}
