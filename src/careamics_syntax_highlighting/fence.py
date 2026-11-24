"""SuperFences formatter that applies the CAREamics Python filter."""

from collections.abc import Callable
from typing import Any

from .semantic import CareamicsPythonSemanticFilter


def format_python(
    source: str,
    language: str,
    class_name: str,
    options: dict[str, Any],
    md: Any,
    **kwargs: Any,
) -> str:
    """Highlight a Python fence using Zensical's configured highlighter."""

    preprocessor = md.preprocessors["fenced_code_block"]
    preprocessor.get_hl_settings()
    highlighter = preprocessor.highlighter
    original_get_lexer: Callable[..., Any] = highlighter.get_lexer

    def get_lexer_with_filter(*args: Any, **inner_kwargs: Any) -> Any:
        lexer, lexer_name = original_get_lexer(*args, **inner_kwargs)
        lexer.add_filter(CareamicsPythonSemanticFilter())
        return lexer, lexer_name

    highlighter.get_lexer = get_lexer_with_filter
    try:
        return preprocessor.highlight(
            src=source,
            language=language,
            options=options,
            md=md,
            classes=kwargs.get("classes"),
            id_value=kwargs.get("id_value", ""),
            attrs=kwargs.get("attrs", {}),
        )
    finally:
        highlighter.get_lexer = original_get_lexer
