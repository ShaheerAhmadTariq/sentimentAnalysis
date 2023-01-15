import React, { useState } from "react";
import { useEffect } from "react";
import Chart from "react-apexcharts";

const SentimentGraph = ({ brandKey, currentDate, prevDate, days, setDays }) => {
  const [options, setOptions] = useState({});
  const [series, setSeries] = useState([]);
  const [loader, setLoader] = useState(true);
  let months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  async function graph() {
    // let graphs = await fetch(`http://localhost:8000/sentimentGraph/`)
    let p_id = JSON.parse(localStorage.getItem("brandList"));
    let { id } = JSON.parse(localStorage.getItem("userEmail"));
    let graphs = await fetch("http://localhost:8000/sentimentGraph/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ p_id: p_id[0].p_id, days, u_id: id }),
    });
    console.log({ p_id: p_id[0].p_id, days, id });

    graphs = await graphs.json();
    console.log(graphs);

    // Dates Sorting
    let Dates = Object.keys(graphs.negative);
    let options = { month: "short", day: "numeric" };

    Dates = Dates.map((elm) => {
      return new Date(elm);
    }).sort();

    Dates = Dates.sort((a, b) => a < b).map((elm) =>
      elm.toLocaleDateString("en-US", options)
    );

    let negativeValues = Object.values(graphs.negative);

    let positiveValues = Object.values(graphs.positive);

    let neutralValues = Object.values(graphs.neutral);

    setOptions({
      chart: {
        type: "line",
        stacked: false,
        fontFamily: "Open-Sans, sans-serif",
      },
      stroke: {
        width: [2, 2, 2],
        curve: "smooth",
      },
      grid: {
        show: true,
        strokeDashArray: 0,
        borderColor: "rgba(0, 0, 0,.3)",
        position: "back",
        xaxis: {
          lines: {
            show: false,
          },
        },
        yaxis: {
          lines: {
            show: true,
          },
        },
        padding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 10,
        },
      },
      colors: ["#73CCE0", "#ACD687", "#E0D45C"],
      labels: Dates,
      markers: {
        size: 1,
        fillColor: ["#ffffff"],
      },
      xaxis: {
        type: "datetime",
        labels: {
          show: true,
          style: {
            colors: "#8CA0A4",
            fontSize: "12px",
          },
        },
        axisBorder: {
          show: true,
          color: "rgba(0,0,0,0.3)",
          height: 1,
          width: "100%",
          offsetX: 0,
          offsetY: 0,
        },
        axisTicks: {
          show: false,
        },
      },
      yaxis: {
        min: 0,
        labels: {
          show: true,
          style: {
            colors: "#8CA0A4",
            fontSize: "12px",
          },
        },
        axisBorder: {
          show: true,
          color: "rgba(0,0,0,0.3)",
          offsetX: 0,
          offsetY: 0,
        },
        title: {
          text: "",
          style: {
            color: "#8CA0A4",
            fontSize: "14px",
            fontWeight: "400",
          },
        },
      },

      tooltip: {
        style: {
          fontSize: "14px",
          fontFamily: "Open-Sans, Sans-serif",
        },
        shared: true,
        intersect: false,
        y: {
          formatter: function (y) {
            if (typeof y !== "undefined") {
              return y.toFixed(0) + " ";
            }
            return y;
          },
        },
      },
    });

    setSeries([
      {
        name: "Number of positive",
        type: "line",
        data: positiveValues,
      },
      {
        name: "Number of negative",
        type: "line",
        data: negativeValues,
      },
      {
        name: "Number of nuetral",
        type: "line",
        data: neutralValues,
      },
    ]);
  }
  useEffect(() => {
    graph();
  }, [days]);

  useEffect(() => {}, []);
  return (
    <>
      <div className="flex h-5 items-center">
        <div className="ml-2 text-sm">
          <label htmlFor="07days" className="font-medium text-green-500">
            07 Days
          </label>
        </div>
        <input
          id="07days"
          aria-describedby="positve-description"
          name="days"
          checked={days === 7 ? true : false}
          type="radio"
          onChange={() => {
            setDays(7);
          }}
          className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
      </div>

      <div className="flex h-5 items-center">
        <div className="ml-2 text-sm">
          <label htmlFor="15days" className="font-medium text-green-500">
            15 Days
          </label>
        </div>
        <input
          id="15days"
          aria-describedby="positve-description"
          checked={days == 15 ? true : false}
          name="days"
          type="radio"
          // checked={positiveCheck}
          onChange={() => {
            setDays(15);
          }}
          className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
      </div>

      <div className="flex h-5 items-center">
        <div className="ml-2 text-sm">
          <label htmlFor="30days" className="font-medium text-green-500">
            30 Days
          </label>
        </div>
        <input
          id="30days"
          aria-describedby="positve-description"
          checked={days == 30 ? true : false}
          name="days"
          type="radio"
          // checked={positiveCheck}
          onChange={() => {
            setDays(30);
          }}
          className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        />
      </div>

      <Chart options={options} series={series} type="line" height={500} />
    </>
  );
};

export default SentimentGraph;
