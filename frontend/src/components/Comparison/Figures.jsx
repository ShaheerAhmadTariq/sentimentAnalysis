import React from "react";
import { useEffect, useState } from "react";

const Figures = ({ brandKey, currentDate, prevDate, data }) => {
  const [graphPositives, setGraphPositives] = useState([]);
  const [graphNegatives, setGraphNegatives] = useState([]);
  const [totalPos, setTotalPos] = useState("");
  const [totalNeg, setTotalNeg] = useState("");
  const [totalNeu, setTotalNeu] = useState("");
  const [total, setTotal] = useState("");

  useEffect(() => {
    // getSentimentGraph();
  }, []);

  useEffect(() => {
    if (graphPositives && graphNegatives) {
      setTotalPos(Math.ceil(graphPositives?.reduce((a, b) => a + b, 0)));
      setTotalNeg(Math.ceil(graphNegatives?.reduce((a, b) => a + b, 0)));
      setTotal(totalPos + Math.abs(totalNeg));
    }
  }, [graphNegatives, graphPositives, totalPos, totalNeg]);

  // get
  async function getSentimentGraph() {
    var gPositives = [];
    var gNegatives = [];
    // encode to scape spaces
    const esc = encodeURIComponent;
    const url = "http://localhost:8000/CountComparison/";
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

    await fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (data) {
          data.data?.map((i) => gPositives.push(i.numberOfPositive));
          data.data?.map((i) => gNegatives.push(i.numberOfNegative));

          setGraphPositives(gPositives);
          setGraphNegatives(gNegatives);
        }
      });
  }
  return (
    <div className="flex flex-col col-span-1">
      <div className="flex flex-col text-center my-2">
        <span className="text-4xl font-[200] my-1">{data?.Total}</span>
        <span className="text-xs text-gray-700 my-1">Total</span>
      </div>
      <div className="flex flex-col text-center my-2">
        <span className="text-4xl font-[200] my-1 text-green-400">
          {data?.Positive}
        </span>
        <span className="text-xs text-gray-700 my-1">Positive</span>
      </div>
      <div className="flex flex-col text-center my-2">
        <span className="text-4xl font-[200] my-1 text-rose-600">
          {data?.Negative}
        </span>
        <span className="text-xs text-gray-700 my-1">Negative</span>
      </div>
      <div className="flex flex-col text-center my-2">
        <span className="text-4xl font-[200] my-1 text-rose-600">
          {data.Neutral}
        </span>
        <span className="text-xs text-gray-700 my-1">Neutral</span>
      </div>
    </div>
  );
};

export default Figures;
