# pylint: skip-file
"""
Interface.
"""


def abstractfunc(func):
    """ Decorator for abstract functions. """
    func.__isabstract__ = True
    return func


class Interface(type):
    """ Metaclass for interfaces. """

    def __init__(self, name, bases, namespace):
        """ Check that all abstract methods are implemented. """
        for base in bases:
            must_implement = getattr(base, "abstract_methods", [])
            class_methods = getattr(self, "all_methods", [])
            for method in must_implement:
                if method not in class_methods:
                    err_str = """Can't create abstract class {name}!
                    {name} must implement abstract method {method}
                    of class {base_class}!""".format(
                        name=name, method=method, base_class=base.__name__
                    )
                    raise TypeError(err_str)

    def __new__(metaclass, name, bases, namespace):
        interface_methods = Interface._get_abstract_methods(namespace)
        namespace["abstract_methods"] = interface_methods
        namespace["all_methods"] = Interface._get_all_methods(namespace)
        cls = super().__new__(metaclass, name, bases, namespace)
        return cls

    def _get_abstract_methods(namespace):
        """ Return a list of abstract methods. """
        return [
            name
            for name, val in namespace.items()
            if callable(val) and getattr(val, "__isabstract__", False)
        ]

    def _get_all_methods(namespace):
        """ Return a list of all methods. """
        return [name for name, val in namespace.items() if callable(val)]
