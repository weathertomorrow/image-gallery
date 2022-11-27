export const withEffect = <T>(arg: T, effect: (arg: T) => unknown): T => {
  effect(arg)
  return arg
}
