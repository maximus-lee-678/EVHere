import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../shared/Navbar';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [fullName, setFullName] = useState('');

  // Handler for login form submission. Transforms fields from useStates into POST fields
  // and sends it to backend. Receives a JSON and acts based on response result.
  async function handleSubmit(e) {
    e.preventDefault();

    // Forms POST header
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username, password: password, email: email, phone_number: phoneNumber, full_name: fullName })
    };

    // Store response
    let response;
    await fetch('/api/create_account', requestOptions)
      .then(res => res.json())
      .then(data => { response = data })
      .catch(err => console.log(err));

    // If success, redirect
    if (response.result) {
      toast.success(response.description);
      // reload page
      window.location.replace('/Login');
    }
    else {
      toast.error(response.description);
    }
  };

  return (
    <div>
      <ToastContainer position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored" />
      <Navbar transparent />
      <main>
        <section className="absolute w-full h-full">
          <div
            className="absolute top-0 w-full h-full bg-gray-900"
            style={{
              backgroundImage:
                "url('login-register.png')",
              backgroundSize: "100%",
              backgroundRepeat: "no-repeat"
            }}
          ></div>
          <div className="container mx-auto px-4 h-full">
            <div className="flex content-center items-center justify-center h-full">
              <div className="w-full lg:w-4/12 px-4">
                <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                  <div className="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                    <div className="text-center mb-3">
                      <h6 className="text-gray-600 text-sm font-bold">
                        Create an account
                      </h6>
                    </div>
                    <form onSubmit={handleSubmit}>
                      <div className="relative w-full mb-3">
                        <label
                          className="block uppercase text-gray-700 text-xs font-bold mb-2"
                          for="emailInput"
                        >
                          Email
                        </label>
                        <input
                          id="emailInput"
                          type="email"
                          className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                          placeholder="janeDoe@email.com"
                          style={{ transition: "all .15s ease" }}
                          value={email} onChange={(event) => setEmail(event.target.value)}
                        />
                      </div>

                      <div className="relative w-full mb-3">
                        <label
                          className="block uppercase text-gray-700 text-xs font-bold mb-2"
                          for="usernameInput"
                        >
                          Username
                        </label>
                        <input
                          id="usernameInput"
                          type="text"
                          className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                          placeholder="janeDoe"
                          style={{ transition: "all .15s ease" }}
                          value={username} onChange={(event) => setUsername(event.target.value)}
                        />
                      </div>

                      <div className="relative w-full mb-3">
                        <label
                          className="block uppercase text-gray-700 text-xs font-bold mb-2"
                          for="passwordInput"
                        >
                          Password
                        </label>
                        <input
                          id="passwordInput"
                          type="password"
                          className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                          placeholder="******************"
                          style={{ transition: "all .15s ease" }}
                          value={password} onChange={(event) => setPassword(event.target.value)}
                        />
                      </div>

                      <div className="relative w-full mb-3">
                        <label
                          className="block uppercase text-gray-700 text-xs font-bold mb-2"
                          for="fullNameInput"
                        >
                          Full Name
                        </label>
                        <input
                          id="fullNameInput"
                          type="text"
                          className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                          placeholder="Jane Doe"
                          style={{ transition: "all .15s ease" }}
                          value={fullName} onChange={(event) => setFullName(event.target.value)}
                        />
                      </div>

                      <div className="relative w-full mb-3">
                        <label
                          className="block uppercase text-gray-700 text-xs font-bold mb-2"
                          for="phoneNumberInput"
                        >
                          Phone Number
                        </label>
                        <input
                          id="phoneNumberInput"
                          type="tel"
                          className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                          placeholder="91234567"
                          style={{ transition: "all .15s ease" }}
                          value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)}
                        />
                      </div>

                      <div className="text-center mt-6">
                        <button
                          className="bg-gray-900 text-white hover:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                          type="submit"
                          style={{ transition: "all .15s ease" }}
                        >
                          Create an account
                        </button>
                      </div>
                    </form>
                    <div className='text-center'>
                      <Link to="/Login" className="mt-6 text-gray-900 hover:text-gray-700">
                        Already have an account?
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section >
      </main >
    </div>


    /* <div>
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
    </div> */

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