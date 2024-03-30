from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    currency: str
    terms: str
    section: str

    @field_validator("price", mode="before")
    def transform_str_to_float(
        cls,
        value: float | str,
    ) -> float:
        if isinstance(value, str):
            return float(value.replace(",", "."))

        return value


class AlgoliaSearchResult(Product):
    object_id: str = Field(
        alias="objectId",
    )
