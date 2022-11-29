from typing import TypeVar

T = TypeVar('T')
def chunk(toChunk: list[T], chunksAmount: int) -> list[list[T]]:
  chunks = [[] for _ in range(0, chunksAmount)]

  for (index, item) in enumerate(toChunk):
    chunks[index % chunksAmount].append(item)

  return chunks
