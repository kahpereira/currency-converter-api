from fastapi import APIRouter, Path, Query
from asyncio import gather
from converter import async_converter
from schemas import ConverterInput, ConverterOutput

router = APIRouter()

# body parameter
@router.post('/converter', response_model=ConverterOutput)
async def converter(body: ConverterInput):
  from_currency = body.from_currency
  to_currencies = body.to_currencies
  price = body.price

  couroutines = []

  for currency in to_currencies:
    coro = async_converter(
      from_currency=from_currency,
      to_currency=currency,
      price=price
    )

    couroutines.append(coro)

  result = await gather(*couroutines)

  return ConverterOutput(
    message='success',
    data=result
  )

# path parameter
# query parameter
@router.get('/converter/async/{from_currency}')
async def converter(
  from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'),
  to_currencies: str = Query(max_length=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'),
  price: float = Query(gt=0)
):
  to_currencies = to_currencies.split(',')

  couroutines = []

  for currency in to_currencies:
    coro = async_converter(
      from_currency=from_currency,
      to_currency=currency,
      price=price
    )

    couroutines.append(coro)

  result = await gather(*couroutines)
  return result