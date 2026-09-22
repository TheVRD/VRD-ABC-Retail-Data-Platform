from datetime import date

from api_ingestion.config.api_config import LANDING_ROOT
from api_ingestion.landing.local_landing_writer import LocalLandingWriter


def main():

    writer = LocalLandingWriter(
        landing_root=LANDING_ROOT
    )

    test_payload = {
        "carts": [
            {
                "id": 1,
                "userId": 10,
                "total": 100
            }
        ],
        "total": 50,
        "skip": 0,
        "limit": 10
    }

    output_path = writer.write_page(
        source_name="sales_api",
        data_entity="carts",
        extraction_date=date(2026, 9, 21),
        run_id="20260921T190000",
        page_number=1,
        payload=test_payload,
    )

    print(f"Landing file created: {output_path}")


if __name__ == "__main__":
    main()