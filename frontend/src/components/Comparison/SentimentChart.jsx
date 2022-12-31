import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";

// import Chart from "react-apexcharts";

const SentimentChart = ({ brandKey, currentDate, prevDate }) => {
  const [graphPositives, setGraphPositives] = useState([]);
  const [graphNegatives, setGraphNegatives] = useState([]);
  const [totalPos, setTotalPos] = useState("");
  const [totalNeg, setTotalNeg] = useState("");
  const [options, setOptions] = useState({
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

  const [series, setSeries] = useState([44, 55]);

  // get

  useEffect(() => {
    async function getSentimentGraph() {
      var gPositives = [];
      var gNegatives = [];
      var gData = [];
      // encode to scape spaces
      const esc = encodeURIComponent;
      const url =
        "https://media-monitoring-tool.herokuapp.com/api/v1/mentions/show-sentiment-chart?";
      const params = {
        keyword: brandKey,
        startDate: prevDate,
        endDate: currentDate,
        sortBy: "publishedAt",
        language: "en",
      };
      // this line takes the params object and builds the query string
      const query = Object.keys(params)
        .map((k) => `${esc(k)}=${esc(params[k])}`)
        .join("&");

      await fetch(url + query)
        .then((res) => res.json())
        .then((data) => {
          if (data) {
            data.data?.map((i) => gPositives.push(i.numberOfPositive));
            data.data?.map((i) => gNegatives.push(i.numberOfNegative));

            setGraphPositives(gPositives);
            setGraphNegatives(gNegatives);
            gData.push(totalPos);
            gData.push(Math.abs(totalNeg));

            setOptions({
              labels: ["Positive", "Negative"],
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

            // set series
            setSeries(gData);
          }
        });
    }
    getSentimentGraph();
  }, [totalNeg, totalPos]);

  useEffect(() => {
    if (graphPositives && graphNegatives) {
      setTotalPos(Math.ceil(graphPositives?.reduce((a, b) => a + b, 0)));
      setTotalNeg(Math.ceil(graphNegatives?.reduce((a, b) => a + b, 0)));
    }
  }, [graphNegatives, graphPositives, totalPos, totalNeg]);

  return (
    <div id="chart">
      <Chart options={options} series={series} type="donut" />
    </div>
  );
};

export default SentimentChart;
