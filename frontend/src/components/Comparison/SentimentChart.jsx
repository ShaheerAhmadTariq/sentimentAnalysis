import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

// import Chart from "react-apexcharts";

const SentimentChart = ({ brandKey, currentDate, prevDate,data }) => {

  const [series, setSeries] = useState([data.news,data.reddit]);
  
  useEffect(()=>{
       setSeries([data.news,data.reddit])
  },[data])
  
  const [options, setOptions] = useState({
    labels:['News',"Reddit"],
    chart: {
      type: "donut",
      hight: 100,
      width: 100,
    },

    dataLabels: {
      enabled: true,
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
