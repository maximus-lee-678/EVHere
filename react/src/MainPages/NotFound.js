// React imports
import React from 'react';
import { Link } from 'react-router-dom';

// Standard imports
import Navbar from '../SharedComponents/Navbar';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-900">
      <Navbar transparent />

      <main>
        <div className="relative pt-16 pb-32 flex content-center items-center justify-center"
          style={{
            height: "75vh"
          }}>

          <div className="container relative mx-auto">
            <div className="items-center flex flex-wrap">
              <div className="w-full lg:w-6/12 px-4 ml-auto mr-auto text-center">
                <div className="pr-12">
                  <h1 className="text-white font-semibold text-5xl">
                    The HTTP 404 Not Found response status code indicates that the server cannot find the requested resource.
                  </h1>
                  <br></br>
                  <Link to="/" className="mt-4 text-lg text-gray-300">
                    This isn't the page you're looking for!
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
