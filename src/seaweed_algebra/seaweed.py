from .base import Base


class Seaweed(Base):
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
