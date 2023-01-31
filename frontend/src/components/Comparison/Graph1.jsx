import React, { useState } from "react";
import { useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import {
  dateSort,
  getArrayOfObjectKeys,
  getArrayOfObjectValues,
} from "../../utils/helperFunctions";

const Graph1 = ({ brandKey, currentDate, prevDate, lineChart }) => {
  const [options, setOptions] = useState({
    chart: {
      type: "line",
      stacked: false,
      fontFamily: "Open-Sans, sans-serif",
    },
    stroke: {
      curve: "straight",
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
    labels: [
      "01/01/2003",
      "02/01/2003",
      "03/01/2003",
      "04/01/2003",
      "05/01/2003",
      "06/01/2003",
      "07/01/2003",
      "08/01/2003",
      "09/01/2003",
      "10/01/2003",
      "11/01/2003",
    ],
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

  const [series, setSeries] = useState([
    {
      name: "Number of positive",
      type: "line",
      data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43],
    },
    {
      name: "Number of negative",
      type: "line",
      data: [23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30],
    },
    {
      name: "Number of nuetral",
      type: "line",
      data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39],
    },
  ]);

  function setSentimentGraph() {
    let labels = getArrayOfObjectKeys(lineChart.project01);
    const valuesProject01 = getArrayOfObjectValues(lineChart.project01);
    const valuesProject02 = getArrayOfObjectValues(lineChart.project02);
    
    setOptions({
      chart: {
        type: "line",
        stacked: false,
        fontFamily: "Open-Sans, sans-serif",
      },
      stroke: {
        curve: "straight",
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
      labels: labels,
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
        name: "Project 01",
        type: "line",
        data: valuesProject01,
      },
      {
        name: "Project 02",
        type: "line",
        data: valuesProject02,
      },
    ]);
  }

  useEffect(() => {
    if (lineChart) {
      setSentimentGraph();
    }
  }, [lineChart]);
  return (
    <ReactApexChart
      options={options}
      series={series}
      type="line"
      height={500}
    />
  );
};

export default Graph1;
