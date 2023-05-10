#!/usr/bin/env python3

import math
import abc
from typing import Any

import Levenshtein


class AttrCorrector(abc.ABC):
    """This class corrects spelling errors in attribute names, treating them as
    if they were spelled correctly. It should not be instantiated directly, you
    must derive a subclass from it in order to use it. The Levenshtein distance
    threshold has a default value of 3, but can optionally be specified in the
    declaration of the subclass like this:

    ```
    class MyClass(AttrCorrector, max_distance=4):
        ...
    ```
    """

    # This is the furthest a misspelling may be from the closest attribute name
    # while still be able to be corrected.
    _DISTANCE_THRESHOLD: int

    def __init_subclass__(cls, max_distance=3) -> None:
        """Initialize the Levenshtein distance threshold in the subclass. This
        method is called every time a subclass of `AttrCorrector` is created."""
        cls._DISTANCE_THRESHOLD = max_distance

    def _correct_attr_name(self, __name: str) -> str:
        """Attempt to correct the spelling of the attribute name and return the
        closest-matching valid attribute name. If no matching attribute name
        within the distance threshold was found, return `__name` unchanged,
        which will raise an `AttributeError` upon use in `__setattr__` or
        `__getattr__`."""

        # The candidates to consider for correct names consist of every method
        # and attribute belonging to the class, including dunder methods.
        targets = dir(self)

        # Check each target name to find which one is closest to the input name.
        # The distance starts out as infinite before any comparisons are made.
        min_dist = math.inf
        closest_name = ""
        for target_name in targets:
            distance = Levenshtein.distance(__name, target_name)
            # Save the new closest word and record its distance from the input.
            if distance < min_dist:
                min_dist = distance
                closest_name = target_name

        # If the word is similar enough to the closest-matching target word,
        # return the match. Otherwise return the word unchanged.
        if min_dist <= self._DISTANCE_THRESHOLD:
            resulting_name = closest_name
        else:
            resulting_name = __name

        return resulting_name

    def __getattr__(self, __name: str):
        """Get the value of the attribute associated with `__name`. Use the
        closest-matching attribute name if `__name` is a misspelling. If no
        matching attribute name within the distance threshold is found, use
        `__name` unchanged, raising an `AttributeError`."""

        attr_name = self._correct_attr_name(__name)
        return object.__getattribute__(self, attr_name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set the value of the attribute associated with `__name` to `__value`.
        Use the closest-matching attribute name if `__name` is a misspelling. If
        no matching attribute name within the distance threshold is found, use
        `__name` unchanged, raising an `AttributeError`."""

        attr_name = self._correct_attr_name(__name)
        super().__setattr__(attr_name, __value)
