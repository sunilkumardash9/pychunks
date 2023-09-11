import os
from functools import partial
from typing import (
    Callable,
    List,
    Optional,
    cast,
)


class GlobalsHelper:
    """Helper to retrieve globals.

    Helpful for global caching of certain variables that can be expensive to load.
    (e.g. tokenization)

    """

    _tokenizer: Optional[Callable[[str], List]] = None
    _stopwords: Optional[List[str]] = None

    # @property
    def tokenizer(self) -> Callable[[str], List]:
        """Get tokenizer."""
        if self._tokenizer is None:
            tiktoken_import_err = (
                "`tiktoken` package not found, please run `pip install tiktoken`"
            )
            try:
                import tiktoken
            except ImportError:
                raise ImportError(tiktoken_import_err)
            enc = tiktoken.get_encoding("gpt2")
            self._tokenizer = cast(Callable[[str], List], enc.encode)
            self._tokenizer = partial(self._tokenizer, allowed_special="all")
        return self._tokenizer  # type: ignore

    @property
    def stopwords(self) -> List[str]:
        """Get stopwords."""
        if self._stopwords is None:
            try:
                import nltk
                from nltk.corpus import stopwords
            except ImportError:
                raise ImportError(
                    "`nltk` package not found, please run `pip install nltk`"
                )

            from llama_index.utils import get_cache_dir

            cache_dir = get_cache_dir()
            nltk_data_dir = os.environ.get("NLTK_DATA", cache_dir)

            # update nltk path for nltk so that it finds the data
            if nltk_data_dir not in nltk.data.path:
                nltk.data.path.append(nltk_data_dir)

            try:
                nltk.data.find("corpora/stopwords")
            except LookupError:
                nltk.download("stopwords", download_dir=nltk_data_dir)
            self._stopwords = stopwords.words("english")
        return self._stopwords