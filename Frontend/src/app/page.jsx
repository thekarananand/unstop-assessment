"use client"

import styles from "./page.module.css";
import { ChangeEvent, useState } from "react";
import backend_url from "@/runtime_variables/backend_url";
import Matrix from "@/components/Matrix";

export default function Home() {

  const [Res,         setRes        ] = useState( { "Booked": [], "State": [], "Message": "" })
  const [SeatsNeeded, setSeatsNeeded] = useState()

  const Reset = async () => {
   
    const response = await fetch( backend_url+'reset/', { method: "GET" } );

    if ( response.ok ) {
      let serverResponse = await response.json();
      setRes( await serverResponse );
    };

  }

  const BookTicket = async () => {

    console.log(backend_url)
   
    const response = await fetch( backend_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
          SeatsNeeded : SeatsNeeded
      })
    });

    if ( response.ok ) {
        let serverResponse = await response.json();
        setRes( await serverResponse );
    };
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        
        <section className={styles.BookingBox}>
          <form>
            <div>
              <label htmlFor="SeatsNeeded">Number of Seats (1 - 7) :</label>
              <input
                autoFocus
                id="SeatsNeeded"
                type="number"
                min="1"
                max="7"
                value={SeatsNeeded}
                placeholder="Seats..."
                onChange={(e) => setSeatsNeeded(e.target.value)}
              />
              <input type="submit" className={styles.btn1} value="Book Ticket" onClick={ (e) => {
                  e.preventDefault();
                  BookTicket();
                }
              }/>
            </div>
            <input type="button" className={styles.btn2} value="Reset" onClick={ (e) => {
                  e.preventDefault();
                  Reset();
                }
              }/>

          </form>
        </section>

        <section>

          <h2> Message Box </h2>
          
          <h1> { Res?.Message} </h1>

          <ul className={styles.SeatBooked}>
            { Res?.Booked && Res?.Booked.map( ( seat, index) => (
              <li key={index++}>
                <span>{seat}</span>
              </li>
            ))}
          </ul>

        </section>

        <section>
          <h2>Seating Layout</h2>
          <Matrix res={Res}/>
        </section>

      </main>
      <footer className={styles.footer}>
        <a href="https://www.github.com/thekarananand/unstop-assessment" target="_blank">
          View Assessment on GitHub
        </a> 
      </footer>
    </div>
  );
}
