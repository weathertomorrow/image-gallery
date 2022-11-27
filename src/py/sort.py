from enum import Enum

class SortOrder(Enum):
  DESC = 'desc'
  ASC = 'asc'

class SortBy(Enum):
  DATE = 'date'
  FILENAME = 'filename'

def getSortOrder(radioOptValue: str) -> SortOrder:
  return SortOrder.ASC if radioOptValue == SortOrder.ASC.value else SortOrder.DESC

def getSortBy(radioOptValue: str) -> SortBy:
  if radioOptValue == SortBy.FILENAME.value:
    return SortBy.FILENAME
  return SortBy.DATE

def getSortParam(sortOrderRadioOptValue: str, sortByRadioOptValue) -> tuple[SortOrder, SortBy]:
  return (getSortOrder(sortOrderRadioOptValue), getSortBy(sortByRadioOptValue))
