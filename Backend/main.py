from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import BookInSingleRow, BookFullCluster, BookLargerCluster
from firebase_utils import getState, getInitialState, setState

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

@app.get("/reset/")
async def reset():

    state = getInitialState()
    setState(state)

    return { 
        "Booked" : [],
        "State"  : getState()
    }

@app.post("/")
async def index(RequestBody: DataScheme):

    state = getState()
    n = RequestBody.SeatsNeeded

    if not ( 1 <= n and n <= 7 ):
        return {
            "Message": f'{n} is out of bound input',
            "Booked" : [],
            "State"  : getState()
        }
    
    if ( sum(state) < n ):
        return {
            "Message": "We don't have Required Capacity",
            "Booked" : [],
            "State"  : getState()
        }
    
    # Check for Rows with Requested Capacity.
    suitable_row = -1;
    suitable_row_state = 8;
    for row in range(len(state)):
        if ( (state[row] >= n) and (suitable_row_state > state[row]) ):
            suitable_row = row
            suitable_row_state = state[row]
            if (state[row] == n):
                break

    # Assigning Seats, if a Row with Requested Capacity is found.
    if ( suitable_row != -1 ):
        
        booked = BookInSingleRow(row=suitable_row, seats=n)

        return { 
            "Message": "Yay! Seats Booked",
            "Booked" : booked,
            "State"  : getState()
        }
    
    # Assigning Seats, in multiple Rows.
    else:
        clusters = {}
        prefix_sum = 0
        begin = -1

        for row in range(len(state)):
            prefix_sum += state[row]
            if begin == -1 and state[row] != 0:
                begin = row
            if ( (prefix_sum != 0) and (state[row] == 0 or (row+1 == len(state))) ):
                clusters[begin] = prefix_sum
                prefix_sum = 0
                begin = -1

        clusters = dict(sorted(clusters.items(), key=lambda item: item[1], reverse=True))

        suitable_single_cluster = -1
        for cluster in clusters:
            if (clusters[cluster] == n):

                booked = BookFullCluster(cluster=cluster)

                return { 
                    "Message": "Yay! Seats Booked 2",
                    "Booked" : booked,
                    "State"  : getState()
                }
            
            elif (clusters[cluster] > n):
                if (suitable_single_cluster == -1):
                    suitable_single_cluster = cluster
                elif ( clusters[suitable_single_cluster] > clusters[cluster] ):
                    suitable_single_cluster = cluster
            
        if (suitable_single_cluster != -1):

            booked = BookLargerCluster(cluster=suitable_single_cluster, seats=n)

            return { 
                "Message": "Yay! Seats Booked 3",
                "Booked" : booked,
                "State"  : getState()
            }

        # Assign Seats in More then one clusters
        else:
            m = n
            booked = []

            for cluster in clusters:
                if ( clusters[cluster] <= m):
                    m -= clusters[cluster]
                    newSeats = BookFullCluster(cluster=cluster)
                    booked.extend(newSeats)
                else:
                    newSeats = BookLargerCluster(cluster=cluster, seats=m)
                    m = 0
                    booked.extend(newSeats)

            print("\n\n##########################")
            print(booked)
            print("##########################\n\n")

            return { 
                "Message": "Yay! Seats Booked 4",
                "Booked" : booked,
                "State"  : getState()
            }
