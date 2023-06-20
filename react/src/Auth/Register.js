// React imports
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputField } from '../SharedComponents/Form';

// API endpoints imports
import { UserInfoRegister } from '../API/API';

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

    const response = await UserInfoRegister(username, password, email, phoneNumber, fullName);

    // If success, redirect
    if (response.success) {
      toast.success(response.api_response);

      // delay 2s
      await new Promise(resolve => setTimeout(resolve, 2000));

      // reload page
      window.location.replace('/Login');
    }
    else {
      toast.error(<div>{response.api_response}<br />{response.reason}</div>);
    }
  };

  return (
    <div>
      <Toast />
      <Navbar transparent />

      <Form elementName="Create an Account" onSubmit={handleSubmit} backgroundImageURL="login-register.png">
        <FormInputField elementName="Email" id="email" placeholder="Enter Email . . ."
          type="email" value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <FormInputField elementName="Username" id="username" placeholder="Enter Username . . ."
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />

        <FormInputField elementName="Password" id="password" placeholder="Enter Password . . ."
          type="password" value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <FormInputField elementName="Full Name" id="full-name" placeholder="Enter Full Name . . ."
          value={fullName}
          onChange={(event) => setFullName(event.target.value)}
        />

        <FormInputField elementName="Phone Number" id="phone-number" placeholder="Enter Phone Number . . ."
          type="tel" value={phoneNumber}
          onChange={(event) => setPhoneNumber(event.target.value)}
        />

        <FormButton elementName="Create" />

        <div className='text-center'>
          <Link to="/Login" className="mt-6 text-gray-900 hover:text-gray-700">
            Already have an account?
          </Link>
        </div>
      </Form>
    </div>
  );
}