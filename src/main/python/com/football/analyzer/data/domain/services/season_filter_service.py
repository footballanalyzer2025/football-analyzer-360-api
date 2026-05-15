from datetime import datetime
from typing import List


class SeasonFilterService:
    SLASH = '/'
    DATE_FORMAT = '%d.%m.%Y'

    def get_season_filter(self, session_type: str, init_date: str) -> List[str]:
        init_dt = datetime.strptime(init_date, self.DATE_FORMAT)

        if self.SLASH in session_type:
            return self._get_range_season_filter(session_type, init_dt)
        return self._get_year_season_filter(session_type, init_dt)

    def _get_range_season_filter(self, session_type: str, init_dt: datetime) -> List[str]:
        end_year = int(session_type.split(self.SLASH)[0])
        current_start = init_dt.year if init_dt.month > 6 else init_dt.year - 1
        return [f"{year}{self.SLASH}{year + 1}" for year in range(current_start, end_year + 1)]

    @staticmethod
    def _get_year_season_filter(session_type: str, init_dt: datetime) -> List[str]:
        end_year = int(session_type)
        return [str(year) for year in range(init_dt.year, end_year + 1)]
