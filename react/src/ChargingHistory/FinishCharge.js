// React imports
import React, { useState, useEffect } from 'react';

// Standard imports
import Toast, { toast } from '../SharedComponents/Toast';
import Form, { FormButton, FormInputField, FormInputSelect } from '../SharedComponents/Form';

// API endpoints imports
import { ChargeHistoryFinish } from '../API/API';

export default function FinishCharge() {
  const userEmail = localStorage.getItem("user_email");

  const [batteryPercentage, setBatteryPercentage] = useState('');
  const [amountPayable, setAmountPayable] = useState('');

  // Function that starts a charge. Called upon form submission.
  async function handleFinish(e) {
    e.preventDefault();

    const response = await ChargeHistoryFinish(userEmail, batteryPercentage, amountPayable);

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

      <Form elementName="Finish Charging History" onSubmit={handleFinish} backgroundImageURL="battery.png">
        <FormInputField elementName="Ending battery percentage" id="battery-end" placeholder="Enter Battery Level . . ."
          type="number" value={batteryPercentage}
          onChange={(event) => setBatteryPercentage(event.target.value)}
        />

        <FormInputField elementName="Amount Payable" id="amount-payable" placeholder="Enter Amount Payable . . ."
          type="number" value={amountPayable}
          onChange={(event) => setAmountPayable(event.target.value)}
        />

        <FormButton elementName={"\"Finish\" Charge"} />
      </Form>
    </div>
  );
}
