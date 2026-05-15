from dataclasses import dataclass
from typing import Optional

from .match_score import MatchScore


@dataclass
class MatchResult:
    first_half: MatchScore
    second_half: MatchScore
    full_time: MatchScore
    has_extra_time: bool = False
    extra_time: Optional[MatchScore] = None
    full_extra_time: Optional[MatchScore] = None
    has_penalties: bool = False
    penalties: Optional[MatchScore] = None

    @classmethod
    def empty(cls) -> 'MatchResult':
        return cls(
            first_half=MatchScore(),
            second_half=MatchScore(),
            full_time=MatchScore()
        )
