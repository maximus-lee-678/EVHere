import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route, Redirect, Navigate, useNavigate, Switch } from 'react-router-dom';

import Dashboard from './MainPages/Dashboard.js';
import NotFound from './MainPages/NotFound.js';
import Login from './Auth/Login.js';
import Register from './Auth/Register.js';

export default function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          {/* This route is for home element with exact path "/", in element props we passes the imported element*/}
          <Route exact path="/" element={<Dashboard />} />
          <Route exact path="/Login" element={<Login />} />
          <Route exact path="/Register" element={<Register />} />

          {/* If any route mismatches the upper route endpoints then, redirect triggers and redirects app to home element with to="/" */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}
