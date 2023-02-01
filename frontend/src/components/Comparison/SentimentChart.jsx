import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

// import Chart from "react-apexcharts";

const SentimentChart = ({ brandKey, currentDate, prevDate, data }) => {
  const [series, setSeries] = useState([data.NewsApi, data.Reddit]);

  useEffect(() => {
    setSeries([data.NewsApi, data.Reddit]);
  }, [data]);

  const [options, setOptions] = useState({
    labels: [
      [
        `NewsApi: ${(
          (data.NewsApi / (data.Reddit + data.NewsApi)) *
          100
        ).toFixed(1)}`,
      ],
      [
        `Reddit: ${((data.Reddit / (data.Reddit + data.NewsApi)) * 100).toFixed(
          1
        )}`,
      ],
    ],
    chart: {
      type: "donut",
      hight: 100,
      width: 100,
    },

    dataLabels: {
      enabled: false,
    },
    legend: {
      show: true,
    },

    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 200,
            height: 200,
          },
          legend: {
            position: "bottom",
          },
        },
      },
    ],
  });

  return (
    <div id="chart">
      <Chart options={options} series={series} type="donut" />
    </div>
  );
};

export default SentimentChart;
