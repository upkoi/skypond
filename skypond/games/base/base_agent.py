from __future__ import absolute_import

class Agent():

    def __init__(self):
        # Used for performance optimization with random agents.
        # When set to true will not cause an observation to be generated
        self.blind = False

    def react(self,observation):
        raise NotImplementedError('implement react in your agent')

    def describe(self):
        raise NotImplementedError('implement describe in your agent')
