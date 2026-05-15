from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class GetAllManagerDatesResponseDTO:
    managers: Dict[str, str]
    count: int
    success: bool = True


@dataclass
class OperationResultDTO:
    success: bool
    message: str
    data: Optional[Dict] = None
