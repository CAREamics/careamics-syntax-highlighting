"""Semantic improvements for Python Pygments tokens."""

from collections.abc import Iterable, Iterator

from pygments.filter import Filter
from pygments.token import Name, Operator, Punctuation, Token


class CareamicsPythonSemanticFilter(Filter):
    """Classify common Python call-site names more precisely."""

    def filter(
        self,
        lexer: object,
        stream: Iterable[tuple[Token, str]],
    ) -> Iterator[tuple[Token, str]]:
        pending: tuple[Token, str] | None = None
        parenthesis_stack: list[bool] = []

        for token, value in stream:
            call_open = False
            if pending is not None:
                pending_token, pending_value = pending

                if token is Punctuation and value == "(" and pending_token in Name:
                    yield Name.Function, pending_value
                    pending = None
                    call_open = True
                elif (
                    token is Operator
                    and value == "="
                    and pending_token in Name
                    and any(parenthesis_stack)
                ):
                    yield Name.Variable, pending_value
                    pending = None
                else:
                    yield pending_token, pending_value
                    pending = None

            if token in Name:
                pending = (token, value)
                continue

            if token is Punctuation:
                if value == "(":
                    parenthesis_stack.append(call_open)
                elif value == ")" and parenthesis_stack:
                    parenthesis_stack.pop()

            yield token, value

        if pending is not None:
            yield pending
