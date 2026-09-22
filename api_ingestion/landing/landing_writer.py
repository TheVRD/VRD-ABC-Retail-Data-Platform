from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path

class LandingWriter(ABC):
    """
    Contract for writing raw API responses to the Landing layer.
    """

    @abstractmethod
    def write_page(
        self,
        *,
        source_name: str,
        data_entity: str,
        extraction_date: date,
        run_id: str,
        page_number: int,
        payload: dict,
    ) -> str:
        raise NotImplementedError