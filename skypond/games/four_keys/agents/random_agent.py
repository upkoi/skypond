from __future__ import absolute_import

from ...base.base_agent import Agent
import numpy as np

from skypond.games.four_keys.four_keys_actions import FourKeysActions

class RandomAgent(Agent):

    def __init__(self,name='random'):
        super().__init__()
        self.name = name
        self.blind = True

    def react(self,observation):
        # Randomly perform one of the available actions
        return np.random.randint(0,len(FourKeysActions))

    def describe(self):
        return {'username':self.name,"eth_address":'', "email":'test@example.com', "description":'Sample Random Agent'}
