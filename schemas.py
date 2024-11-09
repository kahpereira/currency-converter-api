from pydantic import BaseModel, Field, field_validator
from typing import List
import re

class ConverterInput(BaseModel):
  from_currency: str = Field(max_length=3, pattern=r'^[A-Z]{3}$')
  price: float = Field(gt=0)
  to_currencies: List[str]

  @field_validator('to_currencies')
  def validate_to_currencies(cls, value):
    for currency in value:
      if not re.match('^[A-Z]{3}$', currency):
        raise ValueError(f'Invalid currency {currency}')
    return value
  
class ConverterOutput(BaseModel):
  message: str
  data: List[dict]