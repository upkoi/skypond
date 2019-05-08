# How to Contribute to TAIL
Thanks for your interest in improving TAIL. Before opening up an issue or PR please carefully review the information below.

We're currently accepting:

- Bug fixes (see below)
- Significant performance improvements with minimal restructuring
- Well written / meaningful unit tests

In the current stage, helping us raise test coverage and fixing significant bugs are two of the highest value areas for contributing.

We plan on opening up contributions for significant restructuring and features in the future.

## Did you find a bug or significant performance issue?

- Make sure your bug has not already been fixed. Update to the latest version of the master branch and verify that the issue still remains.

- Ensure the bug / performance issue was not already reported by searching on GitHub under Issues. Remember to remove the is:open flag to check for past submissions.

- If you're unable to find an existing issue for the problem, open a new one. Be sure to include as much relevant information as possible and - importantly - an executable test case demonstrating the expected behavior that is not occurring. We recommend using a GitHub gist.

- Your issue must be reproducible. We may close any issues that can't be clearly reproduced.

- In the case of possible performance improvements please use python's timeit and include a summary of the host execution environment.

## Did you fix a bug?

- Review the contribution guidelines below to make sure your submission passes our requirements.

- Open a new pull request with your update. This should go to the master branch.

- Be sure to include the issue number.

- Spelling mistakes are OK but code style PRs will likely be rejected.


## General Contribution Guidelines
To increase the chances that your PR is accepted, make sure your submission meets style guidelines and has adequate code coverage. Also, ensure your submission fits one of the areas that we are currently accepting (see above).

### Style
We loosely follow the [PEP8](https://www.python.org/dev/peps/pep-0008/) [[Alternative Formatting](https://pep8.org/)] guidelines and may reject PRs that significantly deviate from that style. However, we're generally flexible and pragmatic and have made exceptions in a number of areas including line-length.

### Test Coverage
Ideally, your code should have full test coverage. This might be challenging as we're working on increasing test coverage through the rest of the codebase and we'll make reasonable exceptions. We recommend writing supporting tests around the area if possible.

## Competition Timing & Issues
Since this framework is used in live competitions, we ask for special care to be taken to the timing of issues that could impact the outcome of a game. In the 72 hours leading up to a competition please hold any game-altering PRs and issues and submit them only after the game is complete. Check the [schedule](https://midnightfight.ai) for upcoming competitions. We generally will not make execution environment changes shortly before a game begins and this provides us with ample time to review significant issues and respond to them.
