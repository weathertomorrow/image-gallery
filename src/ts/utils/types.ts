import { Literal } from './guards'

export type Nullable<T> = T | null | undefined

export type MutableObject<T extends Literal> = {
  - readonly[key in keyof T]: T[key]
}
