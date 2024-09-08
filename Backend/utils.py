from firebase_utils import getState, getInitialState, setState

def BookInSingleRow(row, seats):

    state = getState()
    begin = -1

    if ( row == 11 ):
        begin = 77 + ( 3 - state[row] + 1)
    else:
        begin = ( row * 7 ) + ( 7 - state[row] + 1)

    state[row] -= seats

    setState(state)
    return list(range( begin, begin + seats ))

def BookFullCluster(cluster):
    
    state = getState()
    row = cluster
    booked = []

    while ( row < 12 and state[row] > 0):
        newSeats = BookInSingleRow(row, state[row])
        booked.extend(newSeats)
        row += 1

    return booked


def BookLargerCluster(cluster, seats):

    
    state = getState()
    row = cluster
    m = seats
    booked = []

    while ( m > 0):
        subset_booked = []
        if ( m > state[row] ):
            m -= state[row]
            newSeats = BookInSingleRow(row, state[row])
        else:
            newSeats = BookInSingleRow(row, m)
            m = 0
        booked.extend(newSeats)
        row += 1

    return booked