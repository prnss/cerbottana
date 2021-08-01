# cerbottana

[![Python 3.9.6](https://img.shields.io/badge/python-3.9.6-blue.svg)](https://www.python.org/downloads/release/python-396/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests status](https://img.shields.io/github/workflow/status/Parnassius/cerbottana/main/master?event=push&label=tests)](https://github.com/Parnassius/cerbottana/actions?query=workflow%3Amain)
[![Codecov](https://img.shields.io/codecov/c/gh/Parnassius/cerbottana/master?token=RYDAXOWCUS)](https://codecov.io/gh/Parnassius/cerbottana)

cerbottana is a [Pokémon Showdown](https://play.pokemonshowdown.com/) bot, originally developed for the room [Italiano](https://play.pokemonshowdown.com/italiano).

## Getting started

These instructions assume you are in the root directory of a cloned cerbottana repository. If you use Windows, it is strongly advised to work within the [WSL](https://docs.microsoft.com/en-us/windows/wsl).

If you are going to test your bot locally, you will also need an active instance of a [Pokémon Showdown server](https://github.com/smogon/pokemon-showdown).

This project uses [Poetry](https://python-poetry.org/) to manage its dependencies, so you will need to install that as well.

### Generating complementary files

Copy `.env-example` into `.env` and edit the file accordingly. Optional environment variables are commented out.

### Running a bot instance

If you are running a local Pokémon Showdown instance, make sure it is active. To start cerbottana, run:

    make run

This will also create a virtual environment and install the necessary dependencies.

To stop the execution, use the command `.kill` on PS (the first character might differ, depending on the configured `COMMAND_CHARACTER`) or just raise a `SIGINT` (`Ctrl + C`) in the console.

## Contributing

Before submitting a pull request, please make sure your code is formatted with `black` and `isort` (`make format` will run those two commands automatically) and that `make test` passes without errors.

The bulk of cerbottana code is plugins (see [plugins reference](plugins/README.md)). Working on a simple plugin is a good first contribution.
