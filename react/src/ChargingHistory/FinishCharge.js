// React imports
import React, { useState, useEffect } from 'react';

// Standard imports
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputField, FormInputSelect } from '../SharedComponents/Form';

// API endpoints imports
import { ChargeHistoryFinish } from '../API/API';

export default function FinishCharge() {
  const userEmail = localStorage.getItem("user_email");

  const [inputKwh, setInputKwh] = useState('0');

  // Function that finishes a charge. Called upon form submission.
  async function handleFinish(e) {
    e.preventDefault();

    const response = await ChargeHistoryFinish(userEmail, inputKwh);

    // result is boolean of status
    if (response.status === 'success') {
      toast.success(response.message);

      // delay 2s
      await new Promise(resolve => setTimeout(resolve, 2000));

      // reload page
      window.location.replace('/');
    } else {
      toast.error(<div>{response.message}<br />{response.reason}</div>);
    }
  }

  return (
    <div>
      <Toast />
      <div className="absolute w-full h-full bg-gray-900">
          <Form elementName="Finish Charging History" onSubmit={handleFinish} backgroundImageURL="battery.png">
            <FormInputField elementName="kWh Final (WiP!)" id="kwh-set" placeholder="Enter kWh . . ."
              type="number" value={inputKwh}
              onChange={(event) => setInputKwh(event.target.value)}
            />

            <FormButton elementName={"\"Finish\" Charge"} />
          </Form>
    </div>
    </div>
  );
}
