import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../shared/Navbar';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [fullName, setFullName] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username, password: password, email: email, phone_number: phoneNumber, full_name: fullName })
    };

    let response;
    await fetch('http://localhost:5000/create_account', requestOptions)
      .then(res => res.json())
      .then(data => { response = data })
      .catch(err => console.log(err));

    alert(response.description);

    if (response.result) {
      // reload page
      window.location.replace('/Login');
    }
  };

  return (
    <div>
      <Navbar />
      <form class="w-full max-w-sm mx-auto mt-6" onSubmit={handleSubmit}>
        <div class="md:flex md:items-center mb-6">
          <div class="md:w-1/3">
            <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-email">
              Email
            </label>
          </div>
          <div class="md:w-2/3">
            <input value={email} onChange={(event) => setEmail(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-email" type="email" placeholder="jane@email.com" />
          </div>
        </div>
        <div class="md:flex md:items-center mb-6">
          <div class="md:w-1/3">
            <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-username">
              Username
            </label>
          </div>
          <div class="md:w-2/3">
            <input value={username} onChange={(event) => setUsername(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-username" type="text" placeholder="janeDoe" />
          </div>
        </div>
        <div class="md:flex md:items-center mb-6">
          <div class="md:w-1/3">
            <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-password">
              Password
            </label>
          </div>
          <div class="md:w-2/3">
            <input value={password} onChange={(event) => setPassword(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-password" type="password" placeholder="******************" />
          </div>
        </div>
        <div class="md:flex md:items-center mb-6">
          <div class="md:w-1/3">
            <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-full-name">
              Full name
            </label>
          </div>
          <div class="md:w-2/3">
            <input value={fullName} onChange={(event) => setFullName(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-full-name" type="text" placeholder="Jane Doe" />
          </div>
        </div>
        <div class="md:flex md:items-center mb-6">
          <div class="md:w-1/3">
            <label class="block text-gray-500 font-bold md:text-left mb-1 md:mb-0 pr-4" for="inline-phone">
              Phone number
            </label>
          </div>
          <div class="md:w-2/3">
            <input value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-cyan-500" id="inline-phone" type="tel" placeholder="91234567" />
          </div>
        </div>
        <div class="md:flex md:items-center">
          <div class="mx-auto">
            <button class="shadow bg-cyan-500 hover:bg-cyan-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded" type="submit">
              Create an account
            </button>
          </div>
        </div>

        <div class="md:flex md:content-center">
          <Link to="/Login" class="mx-auto text-cyan-500 hover:text-cyan-400">Already have an account?</Link>
        </div>
      </form>
    </div>

    /*<form onSubmit={handleSubmit} className="container mx-auto w-fit">

      <div class="flex">
        <label className="w-1/2">
        Username*:</label>
        <input className="w-1/2" type="text" value={username} onChange={(event) => setUsername(event.target.value)} />
      </div>
      
      <div>
        <label>
        Password*:
        <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
      </label>
      </div>
      <div>
      <label>
        Email*:
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
      </label>
      </div>
      <div>
      <label>
        Full Name*:
        <input type="text" value={fullName} onChange={(event) => setFullName(event.target.value)} />
      </label>
      </div>
      <div>
      <label>
        Phone Number:
        <input type="tel" value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} />
      </label>
      </div>
      <button type="submit">Create Account</button>
    </form>*/
  );
}