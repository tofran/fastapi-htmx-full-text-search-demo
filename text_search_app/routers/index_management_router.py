from csv import DictReader

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import PlainTextResponse

from text_search_app.search_indexes.algolia import load_products_into_index
from text_search_app.logging import logger
from text_search_app.models import Product

router = APIRouter(
    prefix="/index",
    tags=["Index management"],
)


@router.post(
    "/upload-csv",
    summary="Upload a list of products, replacing the whole index wi the new ones",
    response_class=PlainTextResponse,
)
async def upload_products(
    csv_file: UploadFile = File(
        title="Products CSV",
        media_type="text/csv",
    ),
):
    logger.info("Uploading products. Re-indexing the application")

    csv_file_contents = await csv_file.read()
    reader = DictReader(
        csv_file_contents.decode().splitlines(),
    )

    products = [
        Product(**row)  # type: ignore
        for row in reader
    ]

    load_products_into_index(products)

    return PlainTextResponse(
        content=f"Successfully indexed {len(products)} products.",
    )
