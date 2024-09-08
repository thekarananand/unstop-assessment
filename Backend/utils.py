def BookInSingleRow(state, row, seats):

    begin = -1

    if ( row == 11 ):
        begin = 77 + ( 3 - state[row] + 1)
    else:
        begin = ( row * 7 ) + ( 7 - state[row] + 1)

    state[row] -= seats

    return [ state, list(range( begin, begin + seats )) ]

def BookFullCluster(state, cluster):
    
    row = cluster
    booked = []

    while ( row < 12 and state[row] > 0):
        [ state, subset_booked ] = BookInSingleRow(state, row, state[row])
        booked.extend(subset_booked)
        row += 1

    return [ state, booked ]


def BookLargerCluster(state, cluster, seats):
    
    row = cluster
    m = seats
    booked = []

    while ( m > 0):
        subset_booked = []
        if ( m > state[row] ):
            m -= state[row]
            [ state, subset_booked ] = BookInSingleRow(state, row, state[row])
        else:
            [ state, subset_booked ] = BookInSingleRow(state, row, m)
            m = 0
        booked.extend(subset_booked)
        row += 1

    return [ state, booked ]