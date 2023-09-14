from typing import Annotated

from fastapi import FastAPI, Path, Query
import requests
from pydantic import BaseModel

app = FastAPI(
    title="Converter"
)

API_KEY = '9d8b939a90c7d2279474a3bc9573ea9a'


class Result(BaseModel):
    result: float


@app.get("/api/rates", response_model=Result)
def rates(source: str = "USD", to: str = "RUB", value: Annotated[float, Query(title="asd", gt=0)] = 1):
    url = f'http://apilayer.net/api/live?access_key={API_KEY}&currencies={to}&source={source}&amount={value}'
    get_url = requests.get(url)
    result_json = get_url.json()
    if not result_json.get('success'):
        return {"Error": "Ошибка! Проверьте правильность названий введенных вами валют"}
    result = result_json.get('quotes').get(source+to)
    return {"result": round(result * value, 2)}

