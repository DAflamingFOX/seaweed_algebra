import pytest

from seaweed_algebra import Meander


def test_meander_validation():
    # The blocks must produce an n by n matrix.
    with pytest.raises(ValueError, match="The sum of the top and bottom"):
        Meander([1, 2], [1, 1])
