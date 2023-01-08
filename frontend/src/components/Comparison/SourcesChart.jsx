import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

// import Chart from "react-apexcharts";

const SourcesChart = ({ brandKey, currentDate, prevDate ,data}) => {

  
  
  const [series, setSeries] = useState([data.Postive,data.Negative]);
  
  useEffect(()=>{
       setSeries([data.Positive,data.Negative])
  },[data])


  const [options, setOptions] = useState({
    labels: ["Positive","Negative"],
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

 


  


  // get
  // async function getSentimentGraph() {
  //   var graphPositives = [];

  //   // encode to scape spaces
  //   const esc = encodeURIComponent;
  //   // const url =
  //   //   "https://media-monitoring-tool.herokuapp.com/api/v1/mentions/show-sentiment-chart?";
  //   const params = {
  //     keyword: brandKey,
  //     startDate: prevDate,
  //     endDate: currentDate,
  //     sortBy: "publishedAt",
  //     language: "en",
  //   };
  //   // this line takes the params object and builds the query string
  //   const query = Object.keys(params)
  //     .map((k) => `${esc(k)}=${esc(params[k])}`)
  //     .join("&");

  //   await fetch(url + query)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       if (data) {
  //         const key = "publishedAt";

  //         const uniqueArr = [
  //           ...new Map(data.data?.map((s) => [s[key], s])).values(),
  //         ];

  //         var arrayUniqueByKey = uniqueArr.slice(0, 6);

  //         arrayUniqueByKey.map((i) => graphPositives.push(i.numberOfPositive));

  //         setOptions({
  //           labels: ["Blogs", "News", "Web", "Videos", "Forums", "Podcasts"],
  //           chart: {
  //             type: "donut",
  //             hight: 100,
  //             width: 100,
  //           },

  //           dataLabels: {
  //             enabled: true,
  //           },
  //           legend: {
  //             show: true,
  //           },

  //           responsive: [
  //             {
  //               breakpoint: 480,
  //               options: {
  //                 chart: {
  //                   width: 200,
  //                   height: 200,
  //                 },
  //                 legend: {
  //                   position: "bottom",
  //                 },
  //               },
  //             },
  //           ],
  //         });

  //         // set series
  //         setSeries(graphPositives);
  //       }
  //     });
  // }

  // useEffect(() => {
  //   getSentimentGraph();
  // }, []);

  return (
    <div id="chart">
      <Chart options={options} series={series} type="donut" />
    </div>
  );
};

export default SourcesChart;
