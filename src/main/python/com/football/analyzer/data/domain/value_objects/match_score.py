from dataclasses import dataclass


@dataclass
class MatchScore:
    home: int = 0
    away: int = 0

    def __sub__(self, other: 'MatchScore') -> 'MatchScore':
        return MatchScore(
            home=self.home - other.home,
            away=self.away - other.away
        )

    def __str__(self):
        return f"{self.home}:{self.away}"
