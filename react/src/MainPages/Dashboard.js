// React imports
import React, { useState, useEffect, useCallback } from 'react';
import { DateTime } from 'luxon';

// Standard imports
import Navbar from "../SharedComponents/Navbar";
import { FormatDateTime, GetDateDiffString } from '../Utils/Time';
import { DashboardCard, ChargingCard } from '../SharedComponents/Card';

// API endpoints imports
import { ChargeHistoryActiveGet } from '../API/API';

export default function Dashboard() {
  const userEmail = localStorage.getItem("user_email");

  const [chargeCurrentDetails, setChargeCurrentDetails] = useState(null);
  const [timeElapsedString, setTimeElapsedString] = useState('');

  // Function that gets user's current charge. Called on page load, populates chargeCurrentDetails.
  const fetchUserChargeCurrent = useCallback(async () => {
    const ResponseCurrent = await ChargeHistoryActiveGet(userEmail);

    // result is boolean of status
    if (ResponseCurrent.status === 'success' && ResponseCurrent.data !== null) {
      setChargeCurrentDetails(ResponseCurrent.data);
      setTimeElapsedString(GetDateDiffString(ResponseCurrent.data.time_start, DateTime.now().toISO()));
    }
  }, [userEmail]);

  useEffect(() => {
    fetchUserChargeCurrent();
  }, [fetchUserChargeCurrent]);

  // Refresh timer every second (1 * 1000) ms
  useEffect(() => {
    setInterval(function () {
      chargeCurrentDetails && setTimeElapsedString(GetDateDiffString(chargeCurrentDetails.time_start, DateTime.now().toISO()));
    }, 1 * 1000);
  }, [chargeCurrentDetails]);

  return (
    <div className="h-screen bg-black">
      <Navbar transparent />

      <main>
        <div className="relative pt-16 pb-32 flex content-center items-center justify-center"
          style={{
            height: "75vh"
          }}>

          <div className="absolute top-0 w-full h-full bg-center bg-cover"
            style={{
              backgroundImage: "url('landing-image.jpg')"
            }}>
            <span id="blackOverlay" className="w-full h-full absolute opacity-75 bg-black"></span>
          </div>
          <div className="container relative mx-auto">
            <div className="items-center flex flex-wrap">
              <div className="w-full lg:w-6/12 px-4 ml-auto mr-auto text-center">
                <h1 className="text-white font-semibold text-3xl md:text-5xl">
                  The best EV charging experience.
                </h1>
                <p className="mt-4 md:text-lg text-gray-300">
                  All your expenses in one place. Mark your favourite chargers, and get recommended charging locations while you're on the go.
                </p>
              </div>

            </div>
          </div>
        </div>

        <section className="bg-black -mt-24">

          {/* Charging status */}
          {chargeCurrentDetails &&
            <ChargingCard elementName="Current Charging Status"
              vName={chargeCurrentDetails.vehicle.name}
              SN={chargeCurrentDetails.vehicle.vehicle_sn}
              currEnergyDrawn={chargeCurrentDetails.charge_current.current_energy_drawn + ' kWh'}
              startTime={FormatDateTime(chargeCurrentDetails.time_start)}
              timeElapsed={timeElapsedString} />}

          {/* Three boxes - charging history, favourites, map */}
          <div className="container mx-auto px-4">
            <div className="flex flex-wrap">

              <DashboardCard lower color="blue" link="/ChargingHistory" elementName="Track your expenses" icon="dollar-sign">
                Tracking your charging time, location, and expenses<br></br>no matter which charger brand you use.
              </DashboardCard>

              <DashboardCard color="red" link="/Favourites" elementName="Favourite chargers" icon="heart">
                Save the location of your favourite EV chargers<br></br>with just a click.
              </DashboardCard>

              <DashboardCard lower color="green" link="/Recommendations" elementName="Get recommendations on the go" icon="map-marker-alt">
                Don't know where to find chargers? Use our map,<br></br>complete with recommendations for you!
              </DashboardCard>

            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
