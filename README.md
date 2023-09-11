[![build status](https://github.com/i13e/osmanthus/actions/workflows/main.yml/badge.svg)](https://github.com/i13e/osmanthus/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/i13e/osmanthus/master.svg)](https://results.pre-commit.ci/latest/github/i13e/osmanthus/master)

![](https://github.com/i13e/osmanthus/assets/62034540/493798b0-39c1-4566-8b99-83941e2e6994)

# Osmanthus

Osmanthus is a sophisticated chess engine that employs advanced algorithms to
provide a challenging and enjoyable playing experience. It offers a range of
features, including self play, puzzle solving, and an intuitive command-line
interface.

## Getting Started

To begin, clone the Git repository by entering the following command in your
terminal/command prompt:

```sh
git clone https://github.com/i13e/osmanthus.git
```

Once you have cloned the repository, navigate to its directory and create a new
Python virtual environment by running:

```sh
cd osmanthus
python -m venv env
```

Activate the environment by running either of the following commands based on
your operating system:

```sh
source env/bin/activate # Mac or Linux
env\Scripts\activate # Windows
```

Next, install the packages listed in the `requirements.txt` file using the
following command:

```sh
pip install -r requirements.txt
```

You're now ready to play or contribute! Once you've finished, you can exit the
environment by running the following command (or simply close the terminal):

```sh
deactivate
```

## Play via CLI

To start the CLI interface, enter the following command:

```sh
python -m osmanthus.cli
```

Moves can be input in Standard Algebraic Notation (SAN) or Universal Chess Interface notation. We
recommend using SAN. If you are new to this notation, we have provided a short guide on our
[wiki page](https://github.com/i13e/osmanthus/wiki/san).

If you are new to playing chess, we suggest checking out [this video](https://www.youtube.com/watch?v=OCSbzArwB10)
to learn the fundamentals.

## Tests

There are unit tests for the engine, CLI, and evaluation modules. We are in the process of adding as
many forced checkmate scenarios as possible. To run the unit tests, ensure that your virtual environment
is active and enter the following command:

```sh
pytest
```

## Contributing

Contributions to Osmanthus are highly appreciated! For suggestions, we recommend looking at any open issues,
particularly those tagged as "Good First Issue" if you are a first-time contributor. We are also opening new
issues related to planned features and bugs that need to be fixed.

When contributing, we ask that you follow the coding style laid out in [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html).

Thank you for your interest in Osmanthus, and we look forward to your contributions!

<!-- 谢谢，李桂花。我愛你 -->
