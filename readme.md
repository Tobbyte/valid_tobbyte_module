# valid_tobbyte_module

A Python decorator just for kicks for validating and type-casting
interactive user input (`input()`).

> _I'm aware that a plain function would make more sense here, given that this
is effectively constrained to input()
— but I'd just learned decorators and had fun with it :)_

`@validate` wraps a prompt-based input function and keeps re-prompting
until a value matching an allowed list (`valid_inputs`) is provided. The input
is automatically converted to the matching type.

## Features

- **Automatic type casting**: Values are cast based on items in `valid_inputs`.
- **First-match order**: Inputs are checked against `valid_inputs` sequentially; the first matching rule wins.
- **Length constraints**: Supports `TypeLengthConstraint` for checking the length of typed entries (e.g. exactly 4 digits). Special character handling applies to `float` entries where `.`, `-`, and `+` are omitted from the length count.
- **Whitespace control**: Leading and trailing whitespaces are trimmed by default (`strip_whitespaces=True`), with an option to preserve raw input.
- **Repeated prompting**: On invalid input, the user is prompted again alongside a display of accepted inputs.
- **Clean exit**: Pressing `Enter` twice in a row (empty input) aborts and returns `None`.

## Installation

No standalone PyPI package — install directly from the Git repo.

In `requirements.txt`:

```
git+https://github.com/Tobbyte/valid_tobbyte_module.git@main#egg=valid_tobbyte_module
```

Then install locally:

```bash
pip install -r requirements.txt
```

## Usage

```python
from valid_tobbyte_module import TypeLengthConstraint, validate


@validate([1, 2, "a", TypeLengthConstraint(max_length=4, data_type=float)])
def get_inp(prompt: str) -> str:
    return input(prompt)


result = get_inp("Input: ")
print(result, type(result))

Example interaction:
  >>> Input: [3]
  ... Accepted inputs: 1, 2, a, float (4)
  >>> Input: [12.34]
  ... 12.34 <class 'float'>
```

## API

### `validate(valid_inputs: list[Any], *, strip_whitespaces: bool = True) -> Callable[[Callable[..., str]], Callable[..., Any | None]]`

Decorator factory. Takes a list of allowed validators and returns the decorator.

**Args:**
- `valid_inputs` (`list[Any]`): List containing any combination of:
  - **Concrete values** (e.g., `1`, `"a"`): Matches exact values after casting.
  - **Bare types** (e.g., `int`, `float`, `str`): Acts as a wildcard matching any input castable to that type.
  - **`TypeLengthConstraint` objects**: Matches inputs of a specific castable type and length.
- `strip_whitespaces` (`bool`): Whether to trim leading/trailing whitespace prior to validation. Defaults to `True`.

**Returns:**
- A decorator wrapping a prompt function (`Callable[..., str]`) returning `Any | None`.

---

### `TypeLengthConstraint(max_length: int, data_type: type = int)`

Dataclass for constraining input length by type.

- `max_length` (`int`): Required length of the input.
- `data_type` (`type`): Target data type to cast to (defaults to `int`).
- **Float handling**: If `data_type=float`, structural characters (`.`, `-`, `+`) are ignored during length counting so only actual digits are evaluated.

## Matching Considerations

- **Evaluation Order**: `valid_inputs` is evaluated strictly sequentially. Placing a broad wildcard like `str` first will consume all inputs before other constraints can be checked.
- **Don't get freaky**: Strings like `"10e3"` evaluate as `10000.0` when cast to `float` and count as 4 characters when non-digit characters are stripped.


## Acknowledgement
- Made with ❤️ and without ai or code completion (except this readme)


## License

This project is licensed under the MIT License.