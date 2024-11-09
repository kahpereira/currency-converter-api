from os import getenv
from dotenv import load_dotenv
import aiohttp
from fastapi import HTTPException

load_dotenv()
API_KEY = getenv('API_KEY')

async def async_converter(from_currency: str, to_currency: str, price: float):
  url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}'

  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url=url) as response:
        data = await response.json()

  except Exception as error:
    raise HTTPException(status_code=400, detail=error)

  if "conversion_rate" not in data:
    raise HTTPException(status_code=400, detail=error)
  exchange_rate = data['conversion_rate']

  return {to_currency: price * exchange_rate}