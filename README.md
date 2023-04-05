# Osmanthus

A chess engine which implements:
- TODO

## Getting Started

To begin with, clone the git repository using the following command in your terminal/command prompt:

```sh
git clone https://github.com/i13e/osmanthus.git
```

Then, navigate to the cloned repository's directory and create a new Python virtual environment by running
the following command:

```sh
cd osmanthus
python -m venv env
```

Activate the environment by running either of the following commands based on your operating system:

```sh
source env/bin/activate # Mac or Linux
env\Scripts\activate # Windows
```

Next, install the packages listed in the `requirements.txt` file using the following command:

```sh
pip install -r requirements.txt
```

You're now ready to play/contribute! Once you're done, simply exit the environment by running the following command:

```sh
deactivate
```

## Play via CLI

Start the interface with:

```sh
python tui.py
```

<!-- Maybe include a gif of the interface here? -->

Moves are input in either Standard Algebraic Notation (SAN) or Universal Chess Interface notation. I would
recommend using SAN; for those new to the notation, I wrote a short guide [here](https://github.com/i13e/osmanthus/wiki/san).

## Tests

There are unit tests for the engine, UI, and evaluation modules. I'm in the process of adding as many forced 
checkmate in 1-3 moves as I can. To run the unit tests, make sure your virtual environment is active and run:

```sh
pytest test/
```

## Contributing
For coding style, I recommend reading [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)
as a place to start.

<!-- 谢谢，李桂花。我愛你 -->
