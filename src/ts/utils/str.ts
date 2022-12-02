export const withSuffix = (sufix: string, name: string): string => {
  return `${name}_${sufix}`
}

export const withPrefix = (prefix: string, name: string): string => withSuffix(name, prefix)

export const toLowerCase = (arg: string): string => arg.toLowerCase()
