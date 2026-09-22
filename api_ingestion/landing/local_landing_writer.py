import json
import os
from datetime import date
from pathlib import Path

from api_ingestion.landing.landing_writer import LandingWriter


class LocalLandingWriter(LandingWriter):
    def __init__(self, landing_root: Path):
        self.landing_root = landing_root

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
        output_directory = (
            self.landing_root
            / source_name
            / str(extraction_date.year)
            / f"{extraction_date.month:02d}"
            / f"{extraction_date.day:02d}"
            / f"run_{run_id}"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = output_directory / f"page_{page_number:03d}.json"

        temp_file_path = file_path.with_suffix(".tmp")

        with temp_file_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(
            temp_file_path,
            file_path,
        )

        return str(file_path)