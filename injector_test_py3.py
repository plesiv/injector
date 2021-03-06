import pytest

from injector import Injector, CallError


def test_implicit_injection_for_python3():
    class A(object):
        pass

    class B(object):
        def __init__(self, a:A):
            self.a = a

    class C(object):
        def __init__(self, b:B):
            self.b = b

    injector = Injector(use_annotations=True)
    c = injector.get(C)
    assert isinstance(c, C)
    assert isinstance(c.b, B)
    assert isinstance(c.b.a, A)


def test_implicit_injection_fails_when_annotations_are_missing():
    class A(object):
        def __init__(self, n):
            self.n = n

    injector = Injector(use_annotations=True)
    with pytest.raises(CallError):
        injector.get(A)


def test_injection_works_in_presence_of_return_value_annotation():
    # Code with PEP 484-compatible type hints will have __init__ methods
    # annotated as returning None[1] and this didn't work well with Injector.
    #
    # [1] https://www.python.org/dev/peps/pep-0484/#the-meaning-of-annotations

    class A:
        def __init__(self, s: str) -> None:
            self.s = s

    def configure(binder):
        binder.bind(str, to='this is string')

    injector = Injector([configure], use_annotations=True)

    # Used to fail with:
    # injector.UnknownProvider: couldn't determine provider for None to None
    a = injector.get(A)

    # Just a sanity check, if the code above worked we're almost certain
    # we're good but just in case the return value annotation handling changed
    # something:
    assert a.s == 'this is string'
