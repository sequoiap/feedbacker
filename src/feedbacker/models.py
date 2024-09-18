from pydantic import BaseModel, ConfigDict


class FeedbackerBase(BaseModel):
    """Base ORM model used by all ORM models."""
    
    model_config = ConfigDict(from_attributes=True)


class Pagination(FeedbackerBase):
    itemsPerPage: int
    page: int
    total: int
