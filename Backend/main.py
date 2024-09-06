from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DataScheme(BaseModel):
    SeatsNeeded: int

@app.post("/")
async def read_root(RequestBody: DataScheme):
    n = RequestBody.SeatsNeeded

    if not ( 1 <= n and n <= 7 ):
        return { "Error": 'SeatsNeeded is out of bound' }
    
    return { "Seat" : [
        0,
        55,
        69,
        79
    ] }