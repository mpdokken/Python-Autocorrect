# Overview

This package allows you to create classes whose attributes are spelling-corrected by deriving from a base class. Any time a class or instance attribute is accessed with a misspelled name, the class will attempt to find the closest valid attribute name and use that instead. It was created in order to gain practice with coding in Python, and is not intended to be useful or practical.

The similarity between the misspelled attribute name and the correct name is calculated using the Levenshtein distance, and a distance threshold may be specified to determine how close the misspelled name must be to a correct name for it to be recognized. If a misspelling is not within the distance threshold for any valid attribute name, an `AttributeError` is raised.

The Levenshtein distance is defined by the number of single-character differences between two strings, including insertions, deletions, and substitutions.

# Installation

Clone the repository, create the virtual environment and activate it.

```bash
python -m virtualenv venv
./venv/Scripts/Activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

# Usage

## Creating the Subclass

To enable spelling correction for a class's attributes, derive the class from the `AttrCorrector` class:

```python
class MyClass(AttrCorrector):
	class_attr = 3
	def __init__(self, value: str):
		self.value = value

	def print_value(self):
		print(self.value)
```

The default distance threshold is 3. You can specify a custom value by including it in the class definition:

```python
class MyClass(AttrCorrector, max_distance=4):
	...
```

## Using the Spelling Correction

The spelling correction works on class attributes, instance attributes, and methods. It is used automatically when the object's attributes are accessed. Each of the misspelled attributes in the below example are successfully corrected.

```python
var = MyClass("abc")

var.valu	# Character deletion
var.vallue	# Character insertion
var.valwe	# Character substitution
var.vllwe	# All 3

var.pint_valu()
MyClass.clss_atr


```

If an attribute name is not within the distance threshold, it cannot be matched with a correct attribute name, and an `AttributeError` is raised.

```python
var.abcdefgh
```

## Limitations

False positive corrections are more likely to occur when the distance threshold is too high, or the class's attributes have short names, such as `Vector.x` or `Vector.y`. Since a misspelling of `x` could have a Levenshtein distance of as little as 1 between it and another single-character name, it's impossible to prevent unintentional corrections.
