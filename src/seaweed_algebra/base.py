from abc import ABC


class Base(ABC):
    def __init__(self, top_blocks: list[int], bottom_blocks: list[int]):

        blocks = top_blocks + bottom_blocks

        if any(block <= 0 for block in blocks):
            raise ValueError(f"""
                             Blocks cannot contain elements <= 0.
                             top blocks: {top_blocks!s}
                             bottom blocks: {bottom_blocks!s}
                             """)

        if sum(top_blocks) != sum(bottom_blocks):
            raise ValueError(f"""
                             The sum of the top and bottom blocks must be equal.
                             top blocks: {top_blocks!s}, sum: {sum(top_blocks)}
                             bottom blocks: {bottom_blocks!s}, sum: {sum(bottom_blocks)}
                             {sum(top_blocks)} != {sum(bottom_blocks)}
                             """)

        self.n = sum(top_blocks)
        self.top_blocks = top_blocks
        self.bottom_blocks = bottom_blocks

    def __eq__(self, other):
        if not isinstance(other, Base):
            return NotImplemented

        return (
            self.top_blocks == other.top_blocks
            and self.bottom_blocks == other.bottom_blocks
        )

    def __str__(self) -> str:
        def create_str(blocks):
            return f"({'|'.join(map(str, blocks))})"
        return f"{create_str(self.top_blocks)} / {create_str(self.bottom_blocks)}"

    def __repr__(self) -> str:
        return f"(top_blocks: {self.top_blocks!s}, bottom_blocks: {self.bottom_blocks!s})"
