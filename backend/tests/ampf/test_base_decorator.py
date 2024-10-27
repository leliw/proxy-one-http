

import pytest
from ampf.base.base_decorator import BaseDecorator


class C:
    def __init__(self) -> None:
        self.x = "x"
    
    def y(self) -> str:
        return "y"
    
    def echo(self, s: str) -> str:
        return s


class D(BaseDecorator[C]):

    def z(self) -> str:
        return "z"
    
def test_decorator():
    # Given: Decorated class C and its decorator D

    # When: Create decorated object
    d = D(C())

    # Then: Decorated class property is obtainable
    assert "x" == d.x
    # Then: Decorated class method without parameters can be called
    assert "y" == d.y()
    # Then: Decorated cladd method with parameters can be called
    assert "hop.hop" == d.echo("hop.hop")
    # Then: Decorator class method without parameters can be called
    assert "z" == d.z()
    # Then: Not existing calling method (neither decorated nor decrator) raise error
    with pytest.raises(AttributeError) as e:
        d.a()
    assert "'D' object has no attribute 'a'" == str(e.value)