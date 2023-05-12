import React, { useState } from 'react';
import Login from '../Auth/Login.js';

export default function Dashboard() {
  const [token, setToken] = useState();

  if (!token) {
    return <Login/>
  }

  return (
    <h2>Dashboard</h2>
  );
}
