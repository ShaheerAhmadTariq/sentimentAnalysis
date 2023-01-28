import React, { useEffect, useState } from "react";
import { MainLayout } from "../../layouts/MainLayout";
import { Card, CardBody } from "../../ui/Card";
import Figures from "../Comparison/Figures";
import SentimentChart from "../Comparison/SentimentChart";
import SourcesChart from "../Comparison/SourcesChart";
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
    getGraphData();
    getData();
  }, []);

  return (
    <MainLayout>
      <div className="bg-white p-10 space-y-10 flex flex-col w-full min-h-screen">
        
        <Card className="my-4">
          <CardBody>
            <p className="text-xl font-bold">Reports Page</p>
            
          </CardBody>
        </Card>
        <div className="col-span-2">
          <div className="">
            {data && (
              <Card className="my-4">
                <h2 className="text-3xl font-semibold ">Sources</h2>
                <CardBody>
                  <p className="capitalize">{data.project01.name}</p>
                  <div className="grid grid-cols-[repeat(auto-fit,_15.666666%)] gap-5 m-auto justify-center">
                    {/* Side Figures */}
                    <Figures
                      data={data.project01}
                      brandKey={brandKey}
                      currentDate={currentDate}
                      prevDate={prevDate}
                    />
                    {/* Pie Chart Positive, Negative */}
                    <div className="col-span-2">
                      <div className="">
                        <SourcesChart
                          brandKey={brandKey}
                          currentDate={currentDate}
                          prevDate={prevDate}
                          data={data.project01}
                        />
                      </div>
                    </div>
                    {/* Pie Chart NewsAPI, Reddit */}
                    <div className="col-span-2">
                      <div className="">
                        <SentimentChart
                          data={data.project01}
                          brandKey={brandKey}
                          currentDate={currentDate}
                          prevDate={prevDate}
                        />
                      </div>
                    </div>
                  </div>
                </CardBody>
              </Card>
            )}
          </div>
        </div>
        {graphs && (
          <>
            <h2 className="text-3xl font-semibold ">
              Number of Mentions
            </h2>
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
            <h2 className="text-3xl font-semibold ">Senitment</h2>
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
      </div>
    </MainLayout>
  );
};

export default Report;
