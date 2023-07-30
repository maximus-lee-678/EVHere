import React from "react";
import Chart from "chart.js/auto";

export default function PieChart() {
  React.useEffect(() => {
    let config = {
      type: "pie",
      data: {
        labels: [
          "Bluecharge",
          "Shell",
          "SPMobility",
          "Plugshare"
        ],
        datasets: [
          {
            label: new Date().getFullYear(),
            fill: false,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)'
            ],
            data: [27, 68, 86, 74]
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: false,
            text: "Vehicles Usage Chart"
          }
        }
      }
    };

    let chartStatus = Chart.getChart("pie-chart"); // <canvas> id
    if (chartStatus !== undefined) {
      chartStatus.destroy();
    }

    let ctx = document.getElementById("pie-chart").getContext("2d");
    window.myBar = new Chart(ctx, config);
  }, []);
  return (
    <div className="w-full px-0 md:px-4">
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full max-w-full flex-grow flex-1">
              <h6 className="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
                Brand
              </h6>
              <h2 className="text-blueGray-700 text-xl font-semibold">
                Yearly brand usage
              </h2>
            </div>
          </div>
        </div>
        <div className="p-2 flex-auto">
          {/* Chart */}
          <div className="relative" style={{ height: "350px" }}>
            <canvas id="pie-chart"></canvas>
          </div>
        </div>
      </div>
    </div>
  );
}
