import { isString, isNil, isPlainObject } from 'lodash'
import { ParsedImage } from './images'

export const isNotNil = <T>(arg: T | null | undefined): arg is T => !isNil(arg)

export type Literal = Record<string, unknown>
export const isLiteral = <T>(
  arg: unknown
): arg is (T extends Literal ? T : Literal) => isPlainObject(arg)

export function isEmpty (arg: string | null | undefined): arg is '' | null | undefined
export function isEmpty<T> (arg: T | null | undefined): arg is null | undefined
export function isEmpty<T> (arg: T): boolean {
  if (arg === null || arg === undefined) {
    return true
  }

  if (isString(arg) && arg.trim() === '') {
    return true
  }

  if (isLiteral(arg) && Object.keys(arg).length === 0) {
    return true
  }

  if (Array.isArray(arg) && arg.length === 0) {
    return true
  }

  return false
}

export const isObjectWithPartialKeys = <T>(
  arg: unknown,
  requiredKeys: Array<keyof T>
): arg is Partial<T> => isLiteral(arg) && requiredKeys.some((key) => key in arg)

export const isArrayOf = <T>(
  arg: unknown,
  guard: (item: unknown) => item is T
): arg is T[] => Array.isArray(arg) && arg.every(guard)

export const isImagePathData = (arg: unknown): arg is ParsedImage => (
  isLiteral(arg) && isObjectWithPartialKeys<ParsedImage>(arg, ['image', 'thumbnail'])
)
