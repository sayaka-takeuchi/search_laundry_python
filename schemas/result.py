from pydantic import BaseModel


class Result(BaseModel):
    result: bool
