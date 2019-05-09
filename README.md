<div align="center">
  <img src="docs/images/logo.png" style="width:40%"><br>
</div>

# SkyPond - A Simple Platform for Reinforcement Learning Competitions
SkyPond is a simple MIT licensed execution engine for multi-agent reinforcement learning competitions and agent evaluation. It was developed by [Upkoi](https://upkoi.com) and is currently in use by [T[AI]L (Tampa AI League)](https://midnightfight.ai) for a recurring midnight reinforcement learning competition.

We think reinforcement learning competitions offer a great opportunity to learn (and are a lot of fun) and SkyPond offers much of the structure needed to build a game out of the box.

This project created from the core execution engine used by T[AI]L and we're working on abstracting away the main game to better allow additional games and more use cases. See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Benefits
- Compatibility with OpenAI Gym.
- Support for Multiple Games (Create Your Own Game)
- First-Class Shared Agent State Handling
- Out of the Box Agent Execution in Docker
- Support for Non-Docker Agents & Hybrid Agent Execution (Run Docker and Non-Docker Agents Together)
- Self-Qualification for Submissions
- Quick Prototyping Helpers for Reward and Multi-Agent Parameters

SkyPond makes it straightforward for competitors to build and test reinforcement learning submissions. Submissions can be tested in a very similar execution model to the competition environment, improving the experience for competitors and competition organizers.

## Requirements
- Python 3
- Full Docker Installation & Support (this excludes virtualized environments like Google Colaboratory)
- Docker Python API
- Ethereum API
- Profanity
- Numpy
- OpenAI Gym
- TQDM

## Installation
Clone the repository and use the setup tool to install:

sudo python3 setup.py install

## Contributing
We're accepting bug fixes and performance improvements. See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Development Roadmap
We think there is a bright future for reinforcement learning competitions and hope to provide helpful tools to make them more accessible to set up and run.

This library is currently being tested by T[AI]L - an experimental reinforcement learning competition - and will likely undergo structural changes in response.

At the moment this library is biased towards T[AI]L and -a starting agent - Four Keys. Eventually, we hope to make the library sufficiently generic and open up support for game submissions. In general, as we identify useful features in T[AI]L we plan to make them generic and bring them over to SkyPond.

## Contact
Please reach out to rob@upkoi.com for any questions or comments.

## Acknowledgments
The idea of using a docker instance for the agent in this project came from Pommerman and Duckietown at NeurIPS 2018. The initial game, Four Keys, is heavily influenced by the starting grid world environments offered by OpenAI Gym as well as the fantastic MiniGrid environment. Lastly, the core PPO engine provided in the RL example builds on top of the Torch AC library.

* [Pommerman](https://github.com/MultiAgentLearning/playground)
* [Duckietown](https://github.com/duckietown)
* [OpenAI Gym](https://github.com/openai/gym)
* [MiniGrid](https://github.com/maximecb/gym-minigrid)
* [Torch AC](https://github.com/lcswillems/torch-ac)
