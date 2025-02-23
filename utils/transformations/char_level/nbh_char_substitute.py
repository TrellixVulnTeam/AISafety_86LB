# !/usr/bin/env python
# coding=UTF-8
"""
@Author: WEN Hao
@LastEditors: WEN Hao
@Description:
@Date: 2021-09-13
@LastEditTime: 2022-04-17

"""

from typing import NoReturn, Optional, List, Any

from utils.transformations.base import CharSubstitute
from utils.misc import DEFAULTS


__all__ = [
    "NeighboringCharacterSubstitute",
]


class NeighboringCharacterSubstitute(CharSubstitute):
    """Transforms an input by replacing its words with a neighboring character substitute."""

    __name__ = "NeighboringCharacterSubstitute"

    def __init__(
        self,
        random_one: bool = True,
        skip_first_char: bool = False,
        skip_last_char: bool = False,
        **kwargs: Any
    ) -> NoReturn:
        """
        Args:
            random_one:
                Whether to return a single word with two characters swapped.
                If not, returns all possible options.
            skip_first_char:
                Whether to disregard perturbing the first character.
            skip_last_char:
                Whether to disregard perturbing the last character.
        """
        super().__init__(**kwargs)
        self.random_one = random_one
        self.skip_first_char = skip_first_char
        self.skip_last_char = skip_last_char

    def _get_candidates(
        self,
        word: str,
        pos_tag: Optional[str] = None,
        num: Optional[int] = None,
    ) -> List[str]:
        """Returns a list containing all possible words with 1 pair of
        neighboring characters swapped."""

        if len(word) <= 1:
            return []

        candidate_words = []

        start_idx = 1 if self.skip_first_char else 0
        end_idx = (len(word) - 2) if self.skip_last_char else (len(word) - 1)

        if start_idx >= end_idx:
            return []

        if self.random_one:
            i = DEFAULTS.RNG.integers(start_idx, end_idx)
            candidate_word = word[:i] + word[i + 1] + word[i] + word[i + 2 :]
            candidate_words.append(candidate_word)
        else:
            for i in range(start_idx, end_idx):
                candidate_word = word[:i] + word[i + 1] + word[i] + word[i + 2 :]
                candidate_words.append(candidate_word)

        if num:
            print(num)
            candidate_words = candidate_words[:num]

        return candidate_words

    @property
    def deterministic(self) -> bool:
        return not self.random_one

    def extra_repr_keys(self) -> List[str]:
        return super().extra_repr_keys() + [
            "random_one",
            "skip_first_char",
            "skip_last_char",
        ]
