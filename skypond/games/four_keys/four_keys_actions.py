from __future__ import absolute_import

from enum import IntEnum

class FourKeysActions(IntEnum):
  NOTHING = 0
  UP = 1
  DOWN = 2
  LEFT = 3
  RIGHT = 4
  DROP_KEY = 6
  ATTACK = 7
