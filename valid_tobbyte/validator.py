"""Validates user input against a list of allowed values."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any


@dataclass(frozen=True)
class TypeLengthConstraint:
    """Transport type and length constraint."""

    max_length: int
    data_type: type = int


def _count_length(raw: str, data_type: type) -> int:
    """Count length of raw input based on data_type."""
    if data_type is float:
        return len(_strip_symbols(raw))
    return len(raw)


def _strip_symbols(raw_user_input: str) -> str:
    """Remove symbols from user input to count digits for floats."""
    replacements = str.maketrans({".": "", "-": "", "+": ""})
    return raw_user_input.translate(replacements)


def _pretty_wrong_input(valid_inputs: list, custom_msg: str = "") -> None:
    """Pretty print allowed inputs when user input is invalid.

    Or print a custom message if provided.
    """
    if custom_msg:
        print(custom_msg)

    def get_by_type(validator: Any) -> str:  # noqa: ANN401
        """Get a string representation of a validator by its type."""
        if isinstance(validator, type):
            return validator.__name__
        if isinstance(validator, TypeLengthConstraint):
            return f"{validator.data_type.__name__} ({validator.max_length})"
        return str(validator)

    # TODO: make more user friendly:
    # 'decimal number' instead of just 'float', etc.
    pretty_valids = ", ".join(get_by_type(valid) for valid in valid_inputs)

    print(f"Accepted inputs: {pretty_valids}")


def validate(
    valid_inputs: list[Any],
    *,
    strip_whitespaces: bool = True,
) -> Callable[[Callable[..., str]], Callable[..., Any | None]]:
    """Enforces input validation and type coercion on user input.

    Wraps a prompt-based input function (e.g., `input()`), continuously
    prompting the user until a valid value from `valid_inputs` is
    provided. The user's string input is dynamically cast against the
    allowed inputs.

    Three kinds of entries are supported in `valid_inputs`:
        - Concrete values (e.g. `1`, `"a"`): matches only that exact
            value, cast to its own type.
        - A bare type (e.g. `int`, `float`, `str`): matches ANY input
            castable to that type ("wildcard").
        - A `TypeLengthConstraint(max_length, data_type)`: matches any
            input castable to `data_type` whose length equals
            `max_length`. For `data_type=float`, the characters `.`,
            `-`, and `+` are excluded from the length count, so only
            actual digits are counted.

    Consider:
    Matching order: `valid_inputs` is processed in its order. The first
    matching entry wins and is returned immediately. A 'str' wildcard as
    first element will match any input. Your responsibility.
    Using multiple `TypeLengthConstraint` (or multiple wildcard types)
    whose accepted inputs overlap is strongly discouraged.
    Don't cry if you try to get funny:
    10e3 will match against TypeLengthConstraint(4, float) and will
    return 10000.0 <class 'float'>. Go figure.

    Whitespace: by default, leading/trailing whitespace is stripped
    from user input before validation (`strip_whitespaces=True`). Pass
    `strip_whitespaces=False` to validate the raw input as-is.

    Features:
        - Automatic type casting based on items in `valid_inputs`.
        - Graceful exit: Pressing 'Enter' twice consecutively
            aborts and returns `None`.
        - Feedback: Displays allowed values on invalid input.

    Args:
        valid_inputs (list[Any]): A list of acceptable values, wildcard
            types, and/or `TypeLengthConstraint` entries (e.g.
            `{1, 2, "a"}`, `{int, TypeLengthConstraint(4, float)}`).
        strip_whitespaces (bool): Whether to strip leading/trailing
            whitespace from user input before validation. Defaults to
            `True`.

    Returns:
        Callable: A decorator with the specified allowed inputs.

    Example:
        >>> @validate([1, 2, "a", TypeLengthConstraint(4, str)])
        >>> def ask(prompt: str) -> str:
        >>>     return input(prompt)
        >>> ask("Enter int or str: ")
        ... [user input:] 3
        >>> Accepted inputs: a, 1, 2, str (4)
        ... [user input:] 23.2
        >>> 23.2 [<class 'str'>]

    """

    def deco(func: Callable[..., str]) -> Callable[..., Any | None]:
        @wraps(func)
        def wrapper(prompt: str) -> Any | None:  # noqa: ANN401
            insist_to_quit = False

            while True:
                raw_user_input = func(prompt)
                if strip_whitespaces:
                    raw_user_input = raw_user_input.strip()

                if not raw_user_input and insist_to_quit:
                    return None
                insist_to_quit = False  # reset

                for valid_inp in valid_inputs:
                    if isinstance(valid_inp, type):
                        # 1. Try matching wildcard types and constraints
                        try:
                            if valid_inp is float:
                                raw_user_input.index(".")
                            return valid_inp(raw_user_input)
                        except (ValueError, TypeError):
                            continue
                    elif isinstance(valid_inp, TypeLengthConstraint):
                        # 2. Match concrete TypeLengthConstraint
                        try:
                            raw_user_input.index(".")
                            typed_user_inp = valid_inp.data_type(
                                raw_user_input,
                            )
                        except (ValueError, TypeError):
                            continue

                        if (
                            _count_length(raw_user_input, valid_inp.data_type)
                            == valid_inp.max_length
                        ):
                            return typed_user_inp
                    else:
                        # 3. Match concrete values (e.g. 1, "a", 3.14)
                        val_type = type(valid_inp)
                        try:
                            typed_user_inp = val_type(raw_user_input)
                            if typed_user_inp in valid_inputs:
                                return typed_user_inp
                        except (ValueError, TypeError):
                            continue

                _pretty_wrong_input(valid_inputs)

                if not raw_user_input:
                    print("Press Enter again to exit.")
                    insist_to_quit = True

        return wrapper

    return deco




if __name__ == "__main__":

    @validate([1, 2, "a", TypeLengthConstraint(4, float)])
    def _get_inp(prompt: str) -> str:
        return input(prompt)

    inp = _get_inp("do inp: ")
    print(inp, type(inp))
