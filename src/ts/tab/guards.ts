import { isString, isNil, isPlainObject } from 'lodash'

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
