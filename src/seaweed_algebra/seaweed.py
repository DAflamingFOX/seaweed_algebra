import matplotlib.pyplot as plt
from matplotlib.axes import Axes


class Seaweed:
    def __init__(self, top_blocks: list[int], bottom_blocks: list[int]):
        """
        Initialize the matrix representation of a seaweed algebra.

        Args:
            top_blocks (list[int]): A list of integers for the horizontal partitions.
            bottom_blocks (list[int]): A list of integers for the vertical partiton.
        """

        # Check that the sum of top == bot because the matrix must be square.
        if sum(top_blocks) != sum(bottom_blocks):
            raise ValueError("The sum of the top and bottom blocks must be equal.")

        self.n = sum(top_blocks)

        self.top_blocks = top_blocks
        self.bottom_blocks = bottom_blocks

    @classmethod
    def from_meander(cls, meander):
        return cls(meander.top_blocks, meander.bottom_blocks)

    def _get_max_row(self) -> list[int]:
        """Get the index of the right-most non-zero element in the row, for all rows.

        Returns:
            list[int]: right-most non-zero column index in each i-th row.
        """
        rows = []
        offset = 0
        for block in self.bottom_blocks:
            for _ in range(block):
                rows.append(offset + block - 1)
            offset += block
        return rows

    def _get_min_row(self) -> list[int]:
        """Get the index of the left-most non-zero element in the row, for all rows.

        Returns:
            list[int]: left-most non-zero column index in each i-th row.
        """
        rows = []
        offset = 0
        for block in self.top_blocks:
            for _ in range(block):
                rows.append(offset)
            offset += block
        return rows
