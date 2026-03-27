from pydantic import BaseModel


class PredictionRequest(BaseModel):
    text: str


class EntryCreate(BaseModel):
    title: str
    description: str