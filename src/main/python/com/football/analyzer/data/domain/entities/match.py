from dataclasses import dataclass

from .team import Team
from ..value_objects.match_result import MatchResult


@dataclass
class Match:
    date: str
    venue: str
    opponent: Team
    result: MatchResult
    match_url: str
    status: str
