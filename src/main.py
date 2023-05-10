"""
This module demonstrates the use of the `AttrCorrector` class and its
spelling-correcting capabilities."""

from corrector import AttrCorrector

class Fruit(AttrCorrector):

    def __init__(self, name: str, color: str, quantity: int) -> None:
        self.name = name
        self.color = color
        self.quantity = quantity

    def desc(self) -> str:
        return f"{self.color} {self.name}: quantity {self.quantity}."
    
val = Fruit('watermelon', 'green', 15)

print("Correctly-spelled attributes")
print("Fruit.name:", val.name)
print("Fruit.color:", val.color)
print("Fruit.quantity:", val.quantity)

print("\nIncorrectly-spelled attributes - the AttrCorrector automatically corrects them.")
print("Fruit.nam:", val.nam)
print("Fruit.nsme:", val.nsme)
print("Fruit.colorrr:", val.colorrr)
print("Fruit.xilir:", val.xilir)
print("Fruit.quany:", val.quany)
print("Fruit.quamfify:", val.quamfify)

# It also corrects function names.
print("Fruit.dec():", val.dec())