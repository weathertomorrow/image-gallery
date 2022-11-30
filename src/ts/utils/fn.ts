export const withEffect = <T>(arg: T, effect: (arg: T) => unknown): T => {
  effect(arg)
  return arg
}

export const call = <T>(arg: T) => <U>(fn: (arg: T) => U) => fn(arg)

export const invoke = (fn: () => unknown): unknown => fn()
