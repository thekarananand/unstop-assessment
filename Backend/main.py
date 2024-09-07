from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class DataScheme(BaseModel):
    SeatsNeeded: int

@app.post("/")
async def read_root(RequestBody: DataScheme):
    n = RequestBody.SeatsNeeded

    if not ( 1 <= n and n <= 7 ):
        return { "Error": f'${n} is out of bound' }
    
    return { "Seat" : [
        0,
        55,
        69,
        79
    ] }