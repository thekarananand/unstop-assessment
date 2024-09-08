from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import BookInSingleRow, BookFullCluster, BookLargerCluster

# state = [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3 ]
state = [ 0, 2, 1, 0, 1, 2, 1, 0, 0, 0, 2, 0 ]

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

@app.get("/reset")
async def reset():
    global state
    state = [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3 ]
    return { "State"  : state }

@app.post("/")
async def index(RequestBody: DataScheme):

    global state
    n = RequestBody.SeatsNeeded

    if not ( 1 <= n and n <= 7 ):
        return { "Error": f'${n} is a valid input' }
    
    if ( sum(state) < n ):
        return {
            "Error"  : "We don't have Reqiured Capacity",
            "Booked" : [],
            "State"  : state
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
        
        [ state, booked ] = BookInSingleRow(state=state, row=suitable_row, seats=n)

        return { 
            "Booked" : booked,
            "State"  : state
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
            if (state[row] == 0):
                clusters[begin]  = prefix_sum


        clusters = dict(sorted(clusters.items(), key=lambda item: item[1], reverse=True))

        suitable_single_cluster = -1
        for cluster in clusters:
            if (clusters[cluster] == n):

                [ state, booked ] = BookFullCluster(state=state, cluster=cluster)

                return { 
                    "Booked" : booked,
                    "State"  : state
                }
            
            elif (clusters[cluster] > n):
                if (suitable_single_cluster == -1):
                    suitable_single_cluster = cluster
                elif ( clusters[suitable_single_cluster] > clusters[cluster] ):
                    suitable_single_cluster = cluster
            
        if (suitable_single_cluster != -1):

            [ state, booked ] = BookLargerCluster(state=state, cluster=cluster, seats=n)

            return { 
                "Booked" : booked,
                "State"  : state
            }

        # Assign Seats in More then one clusters
        else:
            m = n
            booked = []
            for cluster in clusters:
                if ( clusters[cluster] <= m):
                    m -= clusters[cluster]
                    [ state, subset_booked ] = BookFullCluster(state=state, cluster=cluster)
                    
                    booked.extend(subset_booked)
                else:
                    pass
                    [ state, subset_booked ] = BookLargerCluster(state=state, cluster=cluster, seats=m)
                    
                    booked.extend(subset_booked)
            return { 
                "Booked" : booked,
                "State"  : state
            }
