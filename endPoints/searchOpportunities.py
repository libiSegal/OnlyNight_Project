import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
import bepro_api


app = FastAPI()

search_opportunities_router = APIRouter()


class PostBody(BaseModel):
    search_key: str
    starts: int
    check_in: str
    check_out: str


@search_opportunities_router.post('/')
async def search_opportunities(body: PostBody):
    rooms = [{
        "SysRoomCode": "O2A0C",
        "NumRoom": 1,
        "NumCots": 0,
        "NumPax": 2,
        "NumAdt": 2,
        "NumCnn": 0,
        "CnnAge1": 0,
        "CnnAge2": 0,
        "CnnAge3": 0,
        "CnnAge4": 0
    }]
    geo_code = {
        "Latitude": "52.52000659999999",
        "Longitude": "13.404954",
        "PIP": "N"
    }
    bepro_api.search_hotels(body.search_key, geo_code, body.check_in, body.check_out, rooms, body.starts)

    # file = json_reader.get_json_file_names(r'C:\Users\onlyn\PycharmProjects\searchOpportunities\files')[0]
    # return json_reader.read_json_file('files/' + file)


app.include_router(search_opportunities_router, prefix='/search_opportunities')

uvicorn.run(app, host='127.0.0.1', port=8000)
