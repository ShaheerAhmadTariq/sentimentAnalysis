import React, { useEffect, useState } from "react";
import { MainLayout } from "../../layouts/MainLayout";
import SentimentChart from "../Comparison/SentimentChart";
import SentimentGraph from "../Mentions/SentimentGraph";

const Report = () => {
  const [days, setDays] = useState(30);
  const [singleGraphDays, setsingleGraphDays] = useState(30);
  const [data, setData] = useState(undefined);
  var brandKey = JSON.parse(localStorage.getItem("brandList"));
  brandKey = brandKey[0].brandNames;
  brandKey = brandKey?.at(-1);
  const [graphs, setgraphs] = useState(undefined);

  const date = new Date();

  var day = date.getDate();
  var month = date.getMonth() + 1;
  var year = date.getFullYear();
  var currentDate = `${year}-${month}-${day}`;

  // subtraction 25days in current date
  date.setDate(date.getDate() - 25);
  var day2 = date.getDate();
  var month2 = date.getMonth() + 1;
  var year2 = date.getFullYear();
  var prevDate = `${year2}-${month2}-${day2}`;

  async function getData() {
    let { id } = JSON.parse(localStorage.getItem("userEmail"));
    if (!id) {
      alert("No user id found");
      return;
    }
    let resp = await fetch("http://localhost:8000/reportPieChart/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        p_id1: 1,
        u_id: id,
      }),
    });
    resp = await resp.json();
    setData(resp);
  }

  async function getGraphData() {
    try {
      let p_id = JSON.parse(localStorage.getItem("brandList"));
      let { id } = JSON.parse(localStorage.getItem("userEmail"));
      let graphs = await fetch("http://localhost:8000/sentimentGraph/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ p_id: p_id[0].p_id, days, u_id: id }),
      });

      graphs = await graphs.json();
      setgraphs(graphs);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    // getData();
    getGraphData();
  }, []);

  return (
    <MainLayout>
      <div className="bg-white p-10 space-y-10 flex flex-col w-full min-h-screen">
        <h1 className="text-black text-3xl font-bold tracking-wider">
          Reports Page
        </h1>
        {graphs && (
          <>
            <SentimentGraph
              days={singleGraphDays}
              setDays={setsingleGraphDays}
              brandKey={brandKey}
              currentDate={currentDate}
              prevDate={prevDate}
              multiGraph={false}
              graphsValue={graphs}
              displayDateFilter={false}
            />
            <SentimentGraph
              days={days}
              setDays={setDays}
              brandKey={brandKey}
              currentDate={currentDate}
              prevDate={prevDate}
              graphsValue={graphs}
              multiGraph={true}
              displayDateFilter={false}
            />
          </>
        )}

        <div className="col-span-2">
          <div className="">
            {data && (
              <SentimentChart
                data={data.project01}
                brandKey={brandKey}
                currentDate={currentDate}
                prevDate={prevDate}
              />
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default Report;
