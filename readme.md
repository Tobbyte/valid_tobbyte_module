# valid_tobbyte_module

A Python decorator just for kicks for validating and type-casting
interactive user input (`input()`).

`@validate` wraps a prompt-based input function and keeps re-prompting
until a value from an allowed set (`valid_inputs`) is provided. The input
is automatically converted to the matching type.

## Features

- **Automatic type casting**: The target type is inferred from the
  elements of `valid_inputs` (e.g. `int`, `str`, ...).
- **Repeated prompting**: On invalid input, the user is asked again,
  along with a display of the accepted values.
- **Clean exit**: Pressing `Enter` twice in a row (empty input) aborts
  and returns `None`.
- **Typed**: Uses `Any` for the return type, since the concrete type
  depends on runtime data (the elements of `valid_inputs`).

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
from valid_tobbyte_module import validate


@validate({1, 2, "a"})
def get_inp(prompt: str) -> str:
    return input(prompt)


result = get_inp("Input: ")
print(result, type(result))
```

- User enters `1` -> `result` is `1` (as `int`).
- User enters `a` -> `result` is `"a"` (as `str`).
- Invalid input -> re-prompts, showing the accepted values.
- `Enter` pressed twice in a row (with nothing else entered in
  between) -> aborts, return value is `None`.

## API

### `validate(valid_inputs: set[Any]) -> Callable[[Callable[..., str]], Callable[..., Any | None]]`

Decorator factory. Takes a set of allowed values and returns the actual
decorator.

**Args:**
- `valid_inputs` (`set[Any]`): Set of allowed values of arbitrary type,
  e.g. `{1, 2, "a"}`. Each element's type must be constructible from a
  single `str` argument (i.e. `type(element)(some_str)` must work), since
  the raw user input is cast via `type(element)(raw_input)`.

**Returns:**
- A decorator that wraps a prompt-based input function
  (`Callable[..., str]`) and returns a function that yields `Any | None`.

## Design Notes

- The decorator is deliberately scoped to interactive, prompt-based input
  sources (`input()`-like), since it blockingly re-calls the wrapped
  function on invalid input. This retry behavior isn't suitable for other
  sources (API calls, GUI fields, etc.).
- Every element in `valid_inputs` must belong to a type that can be
  constructed from a single `str` argument (e.g. `int`, `str`, `float`).
  Types without such a constructor (or with an incompatible one) will
  simply never match, since the cast attempt raises and is caught.
- At one point (`def wrapper(prompt: str) -> Any | None:`), type checking is
  intentionally suppressed via `noqa: ANN401`, since dynamic
  casting via `type(x)(y)` can't be cleanly statically typed.


  ## Acknowledgement
  - Made with ❤️ and without ai or code completion (except intelliSense) (except this readme)