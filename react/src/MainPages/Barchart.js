import React from "react";
import Chart from "chart.js/auto";

export default function Barchart(props) {

  const { dataExpenses, dataTimeSpent, dataCharged } = props;


  React.useEffect(() => {
    let config = {

      data: {
        datasets: [
          {
            type: "line",
            label: "Expenses ($)",
            fill: false,
            backgroundColor: "rgba(76,81,191, 0.2)",
            borderColor: "#4c51bf",
            data: dataExpenses,
            borderWidth: 2.5,
            pointStyle: 'rectRot',
            tooltip: {
              callbacks: {
                label: function (context) {
                  let label = "Expenses: ";

                  if (context.parsed.y !== null) {
                    label += "$" + Number(Math.round(context.parsed.y + 'e' + 2) + 'e-' + 2).toFixed(2);
                  }

                  return label;
                }
              }
            }
          }, {
            type: "bar",
            label: "Time spent (mins)",
            data: dataTimeSpent,
            fill: false,
            backgroundColor: '#4cbfba',
            borderColor: '#4cbfba',
            barThickness: 8,
            tooltip: {
              callbacks: {
                label: function (context) {
                  let label = "Time spent: ";

                  if (context.parsed.y >= 60) {
                    label += context.parsed.y + " mins (" + (context.parsed.y / 60).toFixed(1) + " hours)";
                  }
                  else {
                    label += context.parsed.y + " mins";
                  }

                  return label;
                }
              }
            }
          }, {
            type: "bar",
            label: "Charged (kWh)",
            data: dataCharged,
            fill: false,
            backgroundColor: '#fca510',
            borderColor: '#fca510',
            barThickness: 8,
            tooltip: {
              callbacks: {
                label: function (context) {
                  let label = "Charged: ";

                  label += context.parsed.y + " kWh";

                  return label;
                }
              }
            }
          },
        ],
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"
        ]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: false,
            text: "Expenses Chart"
          },

        }
      }
    };

    let chartStatus = Chart.getChart("bar-chart"); // <canvas> id
    if (chartStatus !== undefined) {
      chartStatus.destroy();
    }

    let ctx = document.getElementById("bar-chart").getContext("2d");
    window.myBar = new Chart(ctx, config);
  }, [dataExpenses, dataTimeSpent]);
  return (
    <div className="w-full px-0 md:px-4">
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full max-w-full flex-grow flex-1">
              <h6 className="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
                Expenses
              </h6>
              <h2 className="text-blueGray-700 text-xl font-semibold">
                Expenses by month
              </h2>
            </div>
          </div>
        </div>
        <div className="p-2 flex-auto">
          {/* Chart */}
          <div className="relative" style={{ height: "350px" }}>
            <canvas id="bar-chart"></canvas>
          </div>
        </div>
      </div>
    </div>
  );
}
