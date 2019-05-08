from __future__ import absolute_import

from .base_agent import Agent

class CallbackAgent(Agent):
    def __init__(self,react_callback):
        super().__init__()
        self.react_callback = react_callback

    def react(self,observation):
        return self.react_callback(observation)

    def describe(self):
        return dict(username='shim')
