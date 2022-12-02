import { defer } from 'lodash'

export const withEffect = <T>(arg: T, effect: (arg: T) => unknown): T => {
  effect(arg)
  return arg
}

export const call = <T>(arg: T) => <U>(fn: (arg: T) => U) => fn(arg)

export const invoke = (fn: () => unknown): unknown => fn()

type Fun<T, U> = (arg: T) => U
export function flow<A, B> (_funl: Fun<A, B>): Fun<A, B>
export function flow<A, B, C> (_funl: Fun<A, B>, _fun2: Fun<B, C>): Fun<A, C>
export function flow<A, B, C, D> (_funl: Fun<A, B>, _fun2: Fun<B, C>, _fun3: Fun<C, D>): Fun<A, D>
export function flow<A, B, C, D, E> (_funl: Fun<A, B>, _fun2: Fun<B, C>, _fun3: Fun<C, D>, _fun4: Fun<D, E>): Fun<A, E>
export function flow<A, B, C, D, E, F> (_funl: Fun<A, B>, _fun2: Fun<B, C>, _fun3: Fun<C, D>, _fun4: Fun<D, E>, _fun5: Fun<E, F>): Fun<A, F>
export function flow<A, B, C, D, E, F> (_funl: Fun<A, B>, _fun2?: Fun<B, C>, _fun3?: Fun<C, D>, _fun4?: Fun<D, E>, _fun5?: Fun<E, F>): Fun<A, F> {
  const args = arguments
  return (arg: A) => Array.from(args).reduce((prev, curr) => curr(prev), arg)
}

export const prop = <T extends string>(key: T) => <U extends Record<T, unknown>>(arg: U): U[T] => arg[key]

export const eq = (arg: unknown) => (other: unknown) => arg === other

export const makeDefer = (fn: () => void) => () => {
  defer(fn)
}

export const wrapped = (fn: (...args: unknown[]) => void) => () => {
  fn()
}
