import React, { useState, useEffect } from 'react';
import { Icon } from 'leaflet'
import { MapContainer, TileLayer, useMap, Marker, Popup } from 'react-leaflet';

import "leaflet/dist/leaflet.css";
import markerIconPng from "leaflet/dist/images/marker-icon.png"

export default function Dashboard() {
  const handleLogout = () => {
    localStorage.removeItem('user_email');

    // reload page
    window.location.reload();
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <div class="mx-auto">
        <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="submit"
          onClick={handleLogout}>
          Logout
        </button>
      </div>

      <MapContainer center={[1.365, 103.815]} zoom={13} scrollWheelZoom={true} style={{ width: "100%", height: "75vh" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[1.365, 103.815]} icon={new Icon({ iconUrl: markerIconPng, iconSize: [25, 41], iconAnchor: [12, 41] })}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
