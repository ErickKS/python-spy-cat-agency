from functools import lru_cache
from typing import Final, Set

import httpx

CAT_API_URL: Final[str] = 'https://api.thecatapi.com/v1/breeds'

@lru_cache(maxsize=1)
def _breed_set() -> Set[str]:
  resp = httpx.get(CAT_API_URL, timeout=5)
  resp.raise_for_status()
  return {b['name'].lower() for b in resp.json()}


def assert_valid_breed(breed: str) -> None:
  if breed.lower() not in _breed_set():
      raise ValueError(f'Unknown cat breed: {breed}')
