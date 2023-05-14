import React, { useState, useMemo, useEffect } from 'react';
import { Icon } from 'leaflet'
import { MapContainer, TileLayer, useMap, Marker, Popup } from 'react-leaflet';

import "leaflet/dist/leaflet.css";
import markerIconPng from "leaflet/dist/images/marker-icon.png"

export default function Dashboard() {
  const [responseChargerInfo, setResponseChargerInfo] = useState()

  useEffect(() => {
    fetch_charger()

    async function fetch_charger() {
      await fetch('http://localhost:5000/get_chargers')
        .then(res => res.json())
        .then(data => { setResponseChargerInfo(data) })
        .catch(err => console.log(err));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user_email');

    // reload page
    window.location.reload();
  };

  function renderMarkers() {
    let result = [];

    for (var i = 0; i < responseChargerInfo.length; i++) {
      result.push(
        <Marker position={[responseChargerInfo[i].lat, responseChargerInfo[i].long]}
          icon={new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [0, -30] })}>
          <Popup>
            {responseChargerInfo[i].name}
            <br />
            <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded">
              ⭐
            </button>
          </Popup>
        </Marker>
      )
    }
    return result;
  }

  return (
    <div>
      <h2>Dashboard</h2>
      <div class="mx-auto">
        <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="submit"
          onClick={handleLogout}>
          Logout
        </button>
      </div>

      <MapContainer center={[1.365, 103.815]} zoom={12} scrollWheelZoom={true} style={{ width: "100%", height: "75vh" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {responseChargerInfo && renderMarkers()}
      </MapContainer>
    </div>
  );
}
