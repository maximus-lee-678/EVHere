import React, { useState, useMemo, useEffect, useContext } from 'react';
import { BrowserRouter, Routes, Route, Redirect, Navigate, useNavigate, Switch } from 'react-router-dom';
import './App.css';

import Login from './Auth/Login.js';
import Register from './Auth/Register.js';

import NotFound from './MainPages/NotFound.js';

import Dashboard from './MainPages/Dashboard.js';
import Favourites from './MainPages/Favourites.js';
import Recommendations from './MainPages/Recommendations.js';
import Charger from './MainPages/Charger';

export default function App() {
  let userEmail;

  useMemo(() => {
    userEmail = localStorage.getItem("user_email");
  }, []);

  if (userEmail === null && (window.location.pathname != "/Login" || window.location.pathname != "/Register")) {
    // Allow access only to register page, rest of pages lead to login
    return (
      <BrowserRouter>
        <Routes>
          <Route exact path="/Login" element={<Login />} />
          <Route exact path="/Register" element={<Register />} />

          <Route path="*" element={<Login />} />
        </Routes>
      </BrowserRouter>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* This route is for home element with exact path "/", in element props we passes the imported element*/}
        <Route exact path="/" element={<Dashboard />} />

        {/* If any route mismatches the upper route endpoints then, redirect triggers and redirects app to home element with to="/" */}
        <Route path="*" element={<NotFound />} />

        <Route exact path="/Favourites" element={<Favourites />} />
        <Route exact path="/Recommendations" element={<Recommendations />} />
        <Route exact path="/Charger" element={<Charger />} />
      </Routes>
    </BrowserRouter>
  );
}
