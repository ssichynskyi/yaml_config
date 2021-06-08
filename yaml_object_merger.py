from multimethod import multimethod
from typing import Any, Dict, List, Union


Primitive = Union[bool, str, int, float, complex]


@multimethod
def merge(main, complement):
    """
    Merges two results of yaml parsing recursively.

    Idea:
        unlike default implementations like dict.update() this function
        merges given addenda recursively until it comes to a primitive.
        None values are always ignored in favor of valuable alternatives.
        When there's no conflict, the data is merged, not replaced.

    Example:
        main = {
            'name': 'Alex',
            'work': {'address': 'ugly street'},
            'hobbies': ['basketball', 'football'],
            'skills': ['programming', 'testing'],
            'age': 20
        }
        complement = {
            'name': 'Bobby',
            'work': {'address': 'beauty street', 'employed': True},
            'hobbies': ['spearfishing'],
            'skills': 'documenting code',
            'sex': 'Male',
            'age': None
        }
        pprint.pprint(merge_dicts(main, complement))
        >>
        {'age': 20,
         'hobbies': ['basketball', 'football', 'spearfishing'],
         'name': 'Bobby',
         'sex': 'Male',
         'skills': ['programming', 'testing', 'documenting code'],
         'work': {'address': 'beauty street', 'employed': True},
         }

    :param main: a dict to merge to
    :param complement: a dict to merge (values of this dict are preferred over those of main)

    :return: merged dict using above mentioned logic
    """
    ...


@merge.register
def _(main: Any, complement: None):
    """Trivial case when one of merged elements is None."""
    return main


@merge.register
def _(main: None, complement: Any):
    """Trivial case when one of merged elements is None."""
    return complement


@merge.register
def _(main: Primitive, complement: Primitive):
    """Trivial replace case when both merged elements are primitives."""
    return complement


@merge.register
def _(main: List, complement: Primitive):
    """Merge primitive with a list. Trivial case."""
    main.append(complement)
    return main


@merge.register
def _(main: Primitive, complement: List):
    """Merge list to a primitive. Trivial case."""
    complement.append(main)
    return complement


@merge.register
def _(main: List, complement: Dict):
    """Merge list with dict"""
    for index, element in enumerate(main):
        if isinstance(element, Dict):
            common_keys = [key for key in complement.keys() if key in element.keys()]
            if len(common_keys) == 1:
                main[index] = merge(element, complement)
                return main
    main.append(complement)
    return main


@merge.register
def _(main: Dict, complement: List):
    """Merge dict with list"""
    return merge(complement, main)


@merge.register
def _(main: Dict, complement: Dict):
    """Merge two dicts."""
    for k, v in complement.items():
        result = merge(main.get(k, None), v)
        main[k] = result
    return main


@merge.register
def _(main: List, complement: List):
    """Merge two lists"""
    for element in complement:
        main = merge(main, element)
    return main
