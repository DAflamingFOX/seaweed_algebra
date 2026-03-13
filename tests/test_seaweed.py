import pytest

from seaweed_algebra import Seaweed


def test_seaweed_validation():
    # The blocks must produce a n by n matrix.
    with pytest.raises(ValueError, match="The sum of the top and bottom"):
        Seaweed([1, 2], [1, 1])


def test_seaweed_row_calculations():
    sw = Seaweed([4, 1], [2, 1, 2])

    # The left-most valid non-zero column index
    left = [0, 0, 0, 0, 4]
    # The right-most valid non-zero column index
    right = [1, 1, 2, 4, 4]

    assert sw._get_min_row() == left
    assert sw._get_max_row() == right
