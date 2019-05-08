from __future__ import absolute_import

from ...base.base_agent import Agent
from skypond.games.four_keys.four_keys_actions import FourKeysActions

import numpy as np

class RandomAccumulatingAgent(Agent):

    def __init__(self,name='random'):
        super().__init__()
        self.name = name
        self.blind = True

    def react(self,observation):

        # Randomly perform a subset of available actions and attempt to hold on to keys
        action = np.random.choice([FourKeysActions.UP,FourKeysActions.DOWN,FourKeysActions.LEFT,FourKeysActions.RIGHT,FourKeysActions.ATTACK])
        return action

    def describe(self):
        return {'username':self.name,"eth_address":'', "email":'test@example.com', "description":'Sample Random Agent'}
