import React from 'react';
import Navbar from "../SharedComponents/Navbar";
import { Link } from 'react-router-dom';
import { CardContent, CardButton, DashboardCard, ChargingCard } from '../SharedComponents/Card';

export default function Dashboard() {
  return (
    <div className="h-screen bg-gray-300">
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
                <div className="pr-12">
                  <h1 className="text-white font-semibold text-5xl">
                    The best EV charging experience.
                  </h1>
                  <p className="mt-4 text-lg text-gray-300">
                    All your expenses in one place. Mark your favourite chargers, and get recommended charging locations while you're on the go.
                  </p>
                </div>
              </div>

            </div>
          </div>
        </div>



        <section className="bg-gray-300 -mt-24">

          {/* Charging status */}
          <ChargingCard type="CurrentCharging" elementName="Current Charging Status" vName="testing veh 1" SN="SN12345" currPercent="50%" startTime="1/6/2023, 2pm" timeElapsed="50 mins"></ChargingCard>

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
