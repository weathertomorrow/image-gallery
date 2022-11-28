import { isNil } from 'lodash'
import { Nullable } from '../utils/types'

type Coordinates = Readonly<{
  row: number
  column: number
}>

type Dimensions = Readonly<{
  [key in keyof Coordinates as `${key}s`]: Coordinates[key]
}>

const extractButtonPositon = (button: Element): Nullable<Coordinates> => {
  const [column, row] = button.id.replace(/(.*)(\d+_\d+)(.*)/g, '$2').split('_').map(Number)

  if ([column, row].some((coordinate) => isNil(coordinate) || !isFinite(coordinate))) {
    return null
  }

  return { column, row }
}

export const extractGridDimensions = (buttons: Element[]): Dimensions => {
  const dimensions = buttons
    .map(extractButtonPositon)
    .reduce((acc, dimension) => ({
      columns: Math.max(acc?.columns, dimension?.column ?? 0),
      rows: Math.max(acc?.rows, dimension?.row ?? 0)
    }), { columns: 0, rows: 0 })

  return {
    // coordinates start from 0
    columns: dimensions.columns === 0 ? 0 : dimensions.columns + 1,
    rows: dimensions.rows === 0 ? 0 : dimensions.rows + 1
  }
}

export const updateGridCssVariables = (dimensions: Dimensions): void => {
  const root = document.querySelector(':root')

  if (!isNil(root) && root instanceof HTMLElement) {
    root.style.setProperty('--images_gallery__columns', `${dimensions.columns}`)
  }
}
