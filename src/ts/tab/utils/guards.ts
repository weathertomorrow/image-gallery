import { isLiteral, isObjectWithPartialKeys } from '../../utils/guards'
import { ParsedImage } from '../dom/images'

export const isImagePathData = (arg: unknown): arg is ParsedImage => (
  isLiteral(arg) && isObjectWithPartialKeys<ParsedImage>(arg, ['image', 'thumbnail'])
)
