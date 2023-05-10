from dataclasses import dataclass
import unittest
from src.corrector import AttrCorrector


class TestAttrCorrector(unittest.TestCase):
    def setUp(self):
        @dataclass
        class TestClass(AttrCorrector):
            test_attribute: str

            def test_function(self):
                pass

        self.TestClass = TestClass

    def test_valid_get_attr(self):
        """Ensure that getting the value of valid attribute names succeeds with
        no errors."""
        instance = self.TestClass("test_attribute value")
        raised_exception = False

        try:
            instance.test_attribute
            instance.test_function()
        except AttributeError:
            raised_exception = True

        self.assertFalse(
            raised_exception,
            "Getting the value of a valid attribute name raised an AttributeError.",
        )

    def test_misspelled_get_attr(self):
        """Ensure that getting the value of misspelled attributes succeeds with
        no errors. The misspelled names must be within the Levenshtein distance
        threshold for the closest valid attribute name."""

        instance = self.TestClass("test_attribute value")
        
        # Inputs are organized by Levenshtein distance.
        input_groups = {
            1: [
                'test_atXribute',
                'test_attribut',
                'test_attributeX'
            ],
            2: [
                'Xest_attributX',
                'test_attribu',
                'testX_Xattribute'
            ],
            3: [
                'test_atXXibXte',
                'test_atribu',
                'tXest_attributeXX'
            ]
        }

        raised_exception = False
        input = ''
        for group_no in input_groups:
            for input in input_groups[group_no]:
                try:
                    getattr(instance, input)
                    
                except AttributeError:
                    raised_exception = True
        self.assertFalse(
            raised_exception,
            f"Misspelled attribute {input} could not be corrected to a valid attribute name."
        )