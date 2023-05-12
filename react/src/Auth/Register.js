import React, { useState, useRef } from 'react';

export default function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [fullName, setFullName] = useState('');
  
    const handleSubmit = (event) => {
      event.preventDefault();
      console.log(`Submitted form with username: ${username}, password: ${password}, email: ${email}, phone_number: ${phoneNumber}, full_name: ${fullName}`);

      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password, email: email,  phone_number: phoneNumber, full_name: fullName})
    };

    fetch('http://localhost:5000/create_account', requestOptions)
        .then(res => res.json())
        .then(data => {})
        .catch(err => console.log(err));
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <label>
          Username*:
          <input type="text" value={username} onChange={(event) => setUsername(event.target.value)} />
        </label>
        <br />
        <label>
          Password*:
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
        </label>
        <br />
        <label>
          Email*:
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <br />
        <label>
          Full Name*:
          <input type="text" value={fullName} onChange={(event) => setFullName(event.target.value)} />
        </label>
        <br />
        <label>
          Phone Number:
          <input type="tel" value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} />
        </label>
        <br />
        <button type="submit">Create Account</button>
      </form>
    );
}