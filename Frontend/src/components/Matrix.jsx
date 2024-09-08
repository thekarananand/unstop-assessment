import styles from "./Matrix.tsx.module.css";

const Matrix = (props) => {

  const booked = props.res.Booked.sort();
  const state = props.res.State;

  booked.sort((a, b) => a - b)

  const rows = 12;
  const columns = 7;

  var SeatNumber = 1;
  var BookedPtr = 0;

  const matrix = [];
  
  for (let i = 0; i < rows; i++) {
    const row = [];
    for (let j = 0; j < columns; j++) {
      if ( SeatNumber > 80 ) {
        break;
      }

      var css_class = styles.seat

      if ( SeatNumber == booked[BookedPtr] ) {
        css_class += ( " " + styles.booked )
        BookedPtr += 1;
      }

      else {
        if (SeatNumber % 7 == 0){
          if (state[i] == 0) {
            css_class += ( " " + styles.notAval )
          }
        }

        else if ( i == 11 ) {
          if ( (SeatNumber % 7) < (3 - state[i]) + 1 ) {
            css_class += ( " " + styles.notAval )
          }
        }

        else if ( (SeatNumber % 7) < (7 - state[i] + 1) ) {
          css_class += ( " " + styles.notAval )
        }
      }

      row.push(
        <div className={ css_class } key={`${i}-${j}`}> 
          <span>{ SeatNumber }</span>
        </div>
      );

      SeatNumber++;

    }
    matrix.push(row);
  }

  return (
    <div className={styles.MatrixContainer}>
      <div className={styles.matrix}>
        {matrix.map((row, rowIndex) => (
          <div className={styles.rows} key={rowIndex}>{row}</div>
        ))}
      </div>

      <h3>
        Color Code
      </h3>

      <ul>
        <li>
          <div className={ `${styles.seat} ${styles.booked}` }> 
            <span>N</span>
          </div><span>{": Your Seats"}</span>
        </li>
        <li>
          <div className={ `${styles.seat}  ${styles.notAval}` }> 
            <span>N</span>
          </div><span>{": Already Booked Seats"}</span>
        </li>
        <li>
          <div className={ `${styles.seat}` }> 
            <span>N</span>
          </div><span>{": Available Seats"}</span>
        </li>
      </ul>
    </div>
  )
}

export default Matrix