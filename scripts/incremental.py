"""Incremental game"""


from __future__ import annotations

from collections import Counter
import enum
import dataclasses
from typing import Mapping, MutableMapping, Protocol, TypeVar


# TASKS:
# 1) Choose theme:
#   medieval, future, magic, abstract, etc
#   probably future/abstract
# 2) Design core gameplay
# 3) Design code basic structure
#   resource, producer, etc classes

# Basic TypeVars for use in simple generics
T = TypeVar("T")
TCo = TypeVar("TCo", covariant=True)
TContra = TypeVar("TContra", contravariant=True)


class Comparable(Protocol[TContra]):
    """A protocol that provides rich comparison special methods"""

    def __lt__(self, other: TContra) -> bool:
        ...

    def __gt__(self, other: TContra) -> bool:
        ...

    def __le__(self, other: TContra) -> bool:
        ...

    def __ge__(self, other: TContra) -> bool:
        ...


class Combinable(Protocol[TContra, TCo]):
    """A protocol that provides addition and subtraction special methods"""

    def __add__(self, other: TContra) -> TCo:
        ...

    def __sub__(self, other: TContra) -> TCo:
        ...


class MutableCombinable(Combinable[TContra, TCo]):
    """A protocol that provides the combinable protocol, as well as inplace add/sub methods"""

    def __iadd__(self, other: TContra) -> TCo:
        ...

    def __isub__(self, other: TContra) -> TCo:
        ...


class Resource(enum.Enum):
    """Enum of the types of resources"""

    MATERIAL = "material"
    ENERGY = "energy"


class Record(
    Mapping[Resource, int],
    Comparable[Mapping[Resource, int]],
    Combinable[Mapping[Resource, int], "Record"],
):
    """A enhanced mapping that also supports comparisons and addition/subtraction"""


class Inventory(
    Record,
    MutableMapping[Resource, int],
    MutableCombinable[Mapping[Resource, int], "Inventory"],
):
    """A enhanced mutable mapping that also supports comparisions and addition/subtraction"""


class EnhancedCounter(Counter, Inventory):  # pylint: disable=abstract-method
    """A enhanced Counter that is designed to fulfill the Inventory protocol"""

    def __lt__(self, other: Mapping) -> bool:
        """A mapping is < than a other mapping iff
        every key in this mapping is in the other mapping,
        and for every key in this mapping, the value is less than the value of
        the key in the other mapping
        """
        # self is a mapping
        for key in self:
            # checks if not in other map/not less
            # lazy evaluation prevents KeyError
            if key not in other or not self[key] < other[key]:
                return False
        return True

    def __gt__(self, other: Mapping) -> bool:
        """A mapping is > than a other mapping iff
        every key in the other mapping is in this mapping
        and for every key in the other mapping, the value of that key
        in this mapping is greater than the value in the other mapping.
        i.e. this > other iff other < this
        """
        # This logic is the 'opposite' of code in __lt__, with self and other swapped
        for key in other:
            if key not in self or not other[key] < self[key]:
                return False
        return True

    def __le__(self, other: Mapping) -> bool:
        """A mapping is <= than a other mapping iff
        this < other or this == other
        """
        # Check equivalence first because its probably faster
        return self == other or self < other

    def __ge__(self, other: Mapping) -> bool:
        """A mapping is >= than a other mapping iff
        this > other or this == other
        """
        return self == other or self > other

    def __add__(self, other: Mapping) -> EnhancedCounter:
        """This method is already defined by Counter, but in a un-desired method,
        so we directly tie it to Counter.update (desired),
        while also enhancing the type signature
        """
        out = EnhancedCounter()
        out += self
        out += other
        return out

    def __sub__(self, other: Mapping) -> EnhancedCounter:
        """This method is already defined by Counter, but in a un-desired method,
        so we directly tie it to Counter.subtract (desired),
        while also enhancing the type signature
        """
        out = EnhancedCounter()
        out -= self
        out -= other
        return out

    def __iadd__(self, other: Mapping) -> EnhancedCounter:
        """"Inplace add, based on this objects .__add__"""
        self.update(other)
        return self

    def __isub__(self, other: Mapping) -> EnhancedCounter:
        """Inplace sub, based on this objects .__sub__"""
        self.subtract(other)
        return self


@dataclasses.dataclass(frozen=True)
class Recipe:
    """Denotes a 'crafting' recipe, has inputs and outputs with ratios"""

    ingredients: Record
    products: Record


@dataclasses.dataclass()
class Machine:  # name not final: producer? etc
    """A object that can perform recipes at a certain rate"""

    recipe: Recipe
    intake: Inventory
    output: Inventory

    def update(self) -> None:
        """Updates the machine, performs the recipe,
        if sufficient resources are in input inventory,
        places products in output inventory
        """
        if self.intake > self.recipe.ingredients:
            self.intake -= self.recipe.ingredients
            self.output += self.recipe.products
