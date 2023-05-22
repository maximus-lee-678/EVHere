import React, { useState, useMemo, useEffect } from 'react';
import Navbar from "../shared/Navbar";
import Map from "../Map/Map";

export default function Dashboard() {
  return (
    <div>
      <Navbar />
      <h2>Dashboard</h2>
      <Map />
    </div>
  );
}
