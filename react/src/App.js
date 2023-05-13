import React, { useState, useMemo, useEffect, useContext } from 'react';
import logo from './logo.svg';
import './App.css';

import { BrowserRouter, Routes, Route, Redirect, Navigate, useNavigate, Switch } from 'react-router-dom';

import Dashboard from './MainPages/Dashboard.js';
import NotFound from './MainPages/NotFound.js';
import Login from './Auth/Login.js';
import Register from './Auth/Register.js';

export default function App() {
  let loggedInUser;

  useMemo(() => {
    loggedInUser = localStorage.getItem("user_email");
  }, []);

  // console.log(loggedInUser);
  // console.log(window.location.pathname);

  if (loggedInUser === null && (window.location.pathname != "/Login" || window.location.pathname != "/Register")) {
    // Redirect doesnt work properly, can find a much better way
    // return (
    //   <BrowserRouter>
    //     <Navigate to="/Login"/>
    //   </BrowserRouter>
    // );

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
      </Routes>
    </BrowserRouter>
  );
}
