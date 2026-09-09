"""Validates user input against a set of allowed values."""

from collections.abc import Callable
from functools import wraps
from typing import Any


def validate(
    valid_inputs: set[Any],
) -> Callable[[Callable[..., str]], Callable[..., Any | None]]:
    """Enforces input validation and type coercion on user input.

    Wraps a prompt-based input function (e.g., `input()`), continuously
    prompting the user until a valid value from `valid_inputs`
    is provided.
    The user's string input is dynamically cast to the types of the
    allowed inputs.

    Features:
        - Automatic type casting based on items in `valid_inputs`.
        - Graceful exit: Pressing 'Enter' twice consecutively
            aborts and returns `None`.
        - Feedback: Displays allowed values on invalid input.

    Args:
        valid_inputs (Set[Any]): A set containing acceptable values of
        arbitrary types (e.g., `{1, 2, 'a'}`).
        Types are inferred from these values.

    Returns:
        Callable: A decorator with the specified allowed inputs.

    Example:
        >>> @validate({1, 2, "a"})
        ... def ask(prompt: str) -> str:
        ...     return input(prompt)
        >>> ask("Enter int or str: ")

    """

    def deco(func: Callable[..., str]) -> Callable[..., Any | None]:
        @wraps(func)
        def wrapper(prompt: str) -> Any | None:  # noqa: ANN401
            insist_to_quit = False
            while True:
                raw_user_input = func(prompt).strip()

                # Handle abort mechanism on consecutive empty inputs
                if not raw_user_input and insist_to_quit:
                    return None

                insist_to_quit = False

                # Attempt to cast and match against allowed inputs
                for valid_inp in valid_inputs:
                    type_of_val = type(valid_inp)
                    try:
                        typed_user_inp = type_of_val(raw_user_input)
                        print(typed_user_inp)
                    except (ValueError, TypeError):
                        continue
                    else:
                        if typed_user_inp in valid_inputs:
                            return typed_user_inp

                print(f"Accepted inputs: {valid_inputs}")

                if not raw_user_input:
                    print("Press Enter again to exit.")
                    insist_to_quit = True

        return wrapper

    return deco


@validate({1, 2, "a"})
def _get_inp(prompt: str) -> str:
    return input(prompt)


inp = _get_inp("do inp: ")
print(inp, type(inp))
