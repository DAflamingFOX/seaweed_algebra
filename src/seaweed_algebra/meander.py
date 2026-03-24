from enum import Enum

from .base import Base


class Meander(Base):
    class Move(Enum):
        BLOCK_ELIMINATION = "Bl"
        ROTATION_CONTRACTION = "R"
        PURE_CONTRACTION = "P"
        FLIP = "F"
        COMPONENT_DELETION = "C"

        def __str__(self) -> str:
            return self.value

        def __repr__(self) -> str:
            return self.value

    @classmethod
    def from_seaweed(cls, seaweed):
        return cls(seaweed.top_blocks, seaweed.bottom_blocks)

    def _block_elimination(self) -> "Meander":
        """
        If a_1 = 2b_1 then M(g) -> M' of type (b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] == 2 * b[0]:
            return Meander([b[0]] + a[1:], b[1:])

        return self

    def _inv_block_elimination(self) -> "Meander":
        a, b = self.top_blocks, self.bottom_blocks

        return Meander([2 * a[0]] + a[1:], [a[0]] + b)

    def _rotation_contraction(self) -> "Meander":
        """
        If b_1 < a_1 < 2b_1, then M(g) -> M' of type (b_1|a_2|...|a_m) / ((2b_1 - a_1)|b_2|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if b[0] < a[0] and a[0] < 2 * b[0]:
            return Meander([b[0]] + a[1:], [2 * b[0] - a[0]] + b[1:])

        return self

    def _inv_rotation_contraction(self) -> "Meander":

        a, b = self.top_blocks, self.bottom_blocks

        return Meander([2 * a[0] - b[0]] + a[1:], [a[0]] + b[1:])

    def _pure_contraction(self) -> "Meander":
        """
        If a_1 > 2_b1, then M(g) -> M' of type ((a_1 - 2b_1)|b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] > 2 * b[0]:
            return Meander([a[0] - 2 * b[0], b[0]] + a[1:], b[1:])

        return self

    def _inv_pure_contraction(self) -> "Meander":

        a, b = self.top_blocks, self.bottom_blocks

        return Meander([a[0] + 2 * a[1]] + a[2:], [a[1]] + b)

    def _flip(self) -> "Meander":
        """
        If a_1 < b_1, then M(g) -> M' of type (b_1|b_2|...|b_t) / (a_1|...|a_m)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] < b[0]:
            return Meander(b, a)

        return self

    def _inv_flip(self) -> "Meander":

        a, b = self.top_blocks, self.bottom_blocks

        return Meander(b, a)

    def _component_deletion(self) -> tuple["Meander", int]:
        """
        If a_1 = b_1 = c, then M(g) -> M' of type (a_2|...|a_m) / (b_2|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] == b[0]:
            return Meander(a[1:], b[1:]), a[0]

        return self, 0

    def _inv_component_deletion(self, c: int = 1) -> "Meander":

        a, b = self.top_blocks, self.bottom_blocks

        return Meander([c] + a, [c] + b)

    # --- Sequences and Properties

    def _wind_down(self):
        """
        Generator which will continuously apply the next valid move until the Meander is the empty Meander.
        """
        curr = self
        while curr.n > 0:
            a1, b1 = curr.top_blocks[0], curr.bottom_blocks[0]

            if a1 == b1:
                curr, c = curr._component_deletion()
                yield Meander.Move.COMPONENT_DELETION, c
            elif a1 < b1:
                curr = curr._flip()
                yield Meander.Move.FLIP, 0
            elif a1 == 2 * b1:
                curr = curr._block_elimination()
                yield Meander.Move.BLOCK_ELIMINATION, 0
            elif b1 < a1 < 2 * b1:
                curr = curr._rotation_contraction()
                yield Meander.Move.ROTATION_CONTRACTION, 0
            elif a1 > 2 * b1:
                curr = curr._pure_contraction()
                yield Meander.Move.PURE_CONTRACTION, 0
            else:
                raise RuntimeError(f"No valid move. a_1={a1}, b_1={b1}")

    @staticmethod
    def _wind_up(moves: list[Move], deletions: list[int] | None = None):
        if deletions is None:
            deletions = [1] * moves.count(Meander.Move.COMPONENT_DELETION)

        curr = Meander([], [])
        deletion_count = 0
        for move in moves:
            match move:
                case Meander.Move.BLOCK_ELIMINATION:
                    curr = curr._inv_block_elimination()
                case Meander.Move.ROTATION_CONTRACTION:
                    curr = curr._inv_rotation_contraction()
                case Meander.Move.PURE_CONTRACTION:
                    curr = curr._inv_pure_contraction()
                case Meander.Move.FLIP:
                    curr = curr._inv_flip()
                case Meander.Move.COMPONENT_DELETION:
                    curr = curr._inv_component_deletion(deletions[deletion_count])
                    deletion_count += 1

        return curr

    def signature(self) -> list[Move]:
        """
        Calculate the signature of this Meander.
        """

        return [move for move, _ in self._wind_down()]

    def homotopy(self) -> list[int]:
        """
        Calculate the homotopy type of this Meander.
        """

        return [
            c_val
            for move, c_val in self._wind_down()
            if move == Meander.Move.COMPONENT_DELETION
        ]

    def component(self) -> "Meander":
        """
        Calculate the component Meander of this Meander.
        """

        return Meander._wind_up(list(reversed(self.signature())), None)
