// React imports
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

// Standard imports
import Navbar from '../SharedComponents/Navbar';
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputField } from '../SharedComponents/Form';

// API endpoints imports
import { UserInfoLogin } from '../API/API';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Handler for login form submission. Transforms email and password from useStates into POST fields
    // and sends it to backend. Receives a JSON and acts based on response result.
    async function HandleLogin(e) {
        e.preventDefault();

        const response = await UserInfoLogin(email, password);

        // If success returned, change pages
        if (response.status === 'success') {
            // store the user in localStorage
            localStorage.setItem('user_email', email);

            // reload page
            window.location.replace('/');
        } else {
            toast.error(<div>{response.message}<br />{response.reason}</div>);
        }
    }

    return (
        <div>
            <Toast />
            <Navbar transparent/>

            <div className="absolute w-full h-full">
            <div className="absolute top-0 w-full h-full bg-gray-900"
                style={{
                    backgroundImage:
                        `url('login-register.png')`,
                    backgroundSize: "100%",
                    backgroundRepeat: "no-repeat"
                }}></div>
            
            <Form elementName="Sign In" onSubmit={HandleLogin}>
                <FormInputField elementName="Email" id="email" placeholder="Enter Email . . ."
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                />

                <FormInputField elementName="Password" id="password" placeholder="Enter Password . . ."
                    type="password" value={password}
                    onChange={(event) => setPassword(event.target.value)}
                />

                <FormButton elementName="Sign In" />

                <div className='text-center'>
                    <Link to="/Register" className="mt-6 text-gray-900 hover:text-gray-700">
                        Don't have an account? Create one.
                    </Link>
                </div>
            </Form>
            </div>
        </div>
    )
}
