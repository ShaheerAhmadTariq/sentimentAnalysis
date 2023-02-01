import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

const SourcesChart = ({ brandKey, currentDate, prevDate, data }) => {
  const [series, setSeries] = useState([
    data.Postive,
    data.Negative,
    data.Neutral,
  ]);
  const [positive, setPositive] = useState(Number);
  const [negative, setNegative] = useState(Number);
  const [neutral, setNeutral] = useState(Number);

  useEffect(() => {
    setSeries([
      Number(((data.Positive / data.Total) * 100).toFixed(2)),
      Number(((data.Negative / data.Total) * 100).toFixed(2)),
      Number(((data.Neutral / data.Total) * 100).toFixed(2)),
    ]);
  }, [data]);
  const [options, setOptions] = useState({
    labels: [
      [
        `Positive: ${(
          (data.Positive / (data.Positive + data.Negative + data.Neutral)) *
          100
        ).toFixed(1)}`,
      ],
      [
        `Negative: ${(
          (data.Negative / (data.Positive + data.Negative + data.Neutral)) *
          100
        ).toFixed(1)}`,
      ],
      [
        `Neutral: ${(
          (data.Neutral / (data.Positive + data.Negative + data.Neutral)) *
          100
        ).toFixed(1)}`,
      ],
    ],
    chart: {
      type: "donut",
      hight: 100,
      width: 100,
    },
    plotOptions: {
      pie: {
        customScale: 1,
      },
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
            width: 250,
            height: 250,
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

export default SourcesChart;
