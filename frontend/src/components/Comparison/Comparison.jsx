import React from "react";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import { MainLayout } from "../../layouts/MainLayout";
import { Card, CardBody } from "../../ui/Card";
import Graph1 from "./Graph1";
import Figures from "./Figures";
import SourcesChart from "./SourcesChart";
import SentimentChart from "./SentimentChart";
import Filters from "./Filters";
import ProjectsModal from "./ProjectsModal";
import { Loader } from "../../ui/Loader";

const Comparison = () => {
  const [open, setOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(undefined);
  const [brandList, setBrandList] = useState([]);
  const [selectedProjects, setSelectedProjects] = useState([]);
  const [lineChartData, setlineChartData] = useState();

  var brandKey = JSON.parse(localStorage.getItem("brandList"));
  brandKey = brandKey && brandKey[0].brandNames;
  brandKey = brandKey?.at(-1).replace(/^\s+/g, "");

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

  useEffect(() => {
    if (brandList?.length > 1) setIsLoading(false);
  }, [brandList]);

  // Function to get pie chart data of given project ids'
  async function getData() {
    let { id } = JSON.parse(localStorage.getItem("userEmail"));
    if (!id) {
      alert("No user id found");
      return;
    }
    let resp = await fetch("http://localhost:8000/CountComparison/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        p_id1: selectedProjects[0],
        p_id2: selectedProjects[1],
        days: 30,
        u_id: id,
      }),
    });
    resp = await resp.json();
    setData(resp);
  }

  // Single Line Chart API Call
  async function getComparisonLineChart() {
    let { id } = JSON.parse(localStorage.getItem("userEmail"));
    try {
      const res = await fetch("http://localhost:8000/comaprisonLineChart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          u_id: id,
          p_id1: selectedProjects[0],
          p_id2: selectedProjects[1],
          days: 30,
        }),
      });
      const lineChart = await res.json();
      setlineChartData(lineChart);
    } catch (error) {
      console.log(error);
    }
  }

  async function getProjects() {
    let { id } = JSON.parse(localStorage.getItem("userEmail"));
    if (!id) {
      alert("No user id found");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/getProjects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ u_id: id }),
      });
      const data = await res.json();
      setBrandList(data);
    } catch (error) {
      console.log(error);
    }
  }

  // Fetch single line comparison project on component load
  useEffect(() => {
    getProjects();
  }, []);

  // Fetches all the projects for comparison on every change of `secondProject` value
  useEffect(() => {
    if (selectedProjects.length === 2) {
      // Must be called after the above function
      getComparisonLineChart();
      getData();
    }
  }, [selectedProjects]);
  if (!brandList)
    return (
      <MainLayout className="bg-white h-screen">
        <h1 className="text-center text-black text-2xl">
          Please select a project first from Dashboard
        </h1>
      </MainLayout>
    );

  return (
    <MainLayout>
      {brandList?.length <= 1 ? (
        <div className="m-4 min-h-screen">
          <Card>
            <CardBody>
              You have only one project. Create one more project to compare!{" "}
              <Link to="/monitor">
                <button
                  type="button"
                  className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-3 py-2 text-sm font-medium leading-4 text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  Create Project
                </button>
              </Link>
            </CardBody>
          </Card>
        </div>
      ) : (
        <div className="m-4 min-h-screen">
          {isLoading ? (
            <Loader className="text-indigo-600" />
          ) : (
            <>
              <ProjectsModal
                open={open}
                setOpen={setOpen}
                brandList={brandList}
                isLoading={isLoading}
                selectedProjects={selectedProjects}
                setSelectedProjects={setSelectedProjects}
              />
              <Card className="my-4">
                <CardBody>
                  <Filters open={open} setOpen={setOpen} />
                </CardBody>
              </Card>
              {/* Main Graph Card */}
              {selectedProjects.length === 2 && (
                <Card>
                  <CardBody>
                    <div>
                      <p className="capitalize">{brandKey}</p>
                      <Graph1
                        lineChart={lineChartData}
                        brandKey={brandKey}
                        currentDate={currentDate}
                        prevDate={prevDate}
                      />
                    </div>
                  </CardBody>
                </Card>
              )}
              {/* {secondProject?.length > 0 ? (
                <Card className="my-4">
                  <CardBody>
                    <div>
                      <p className="capitalize">{secondProject}</p>
                      <Graph1
                        brandKey={secondProject}
                        currentDate={currentDate}
                        prevDate={prevDate}
                      />
                    </div>
                  </CardBody>
                </Card>
              ) : null} */}

              {data ? (
                <>
                  {/* Project01 */}
                  <Card className="my-4">
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
                  {/* Project02 */}
                  <Card className="my-4">
                    <CardBody>
                      <p className="capitalize">{data.project02.name}</p>

                      <div className="grid grid-cols-[repeat(auto-fit,_15.666666%)] gap-5 m-auto justify-center">
                        {/* Side Figures */}
                        <Figures
                          data={data.project02}
                          brandKey={brandKey}
                          currentDate={currentDate}
                          prevDate={prevDate}
                        />
                        {/* Pie Chart for Positive, Negative */}
                        <div className="col-span-2">
                          <div className="">
                            <SourcesChart
                              brandKey={brandKey}
                              currentDate={currentDate}
                              prevDate={prevDate}
                              data={data.project02}
                            />
                          </div>
                        </div>
                        {/* Pie Chart for NewsAPI, Reddit */}
                        <div className="col-span-2">
                          <div className="">
                            <SentimentChart
                              data={data.project02}
                              brandKey={brandKey}
                              currentDate={currentDate}
                              prevDate={prevDate}
                            />
                          </div>
                        </div>
                      </div>
                    </CardBody>
                  </Card>
                </>
              ) : null}

              {/* {secondProject?.length > 0 ? (
                <Card className="my-4">
                  <CardBody>
                    <p className="capitalize">{secondProject}</p>

                    <div className="grid grid-cols-[repeat(auto-fit,_15.666666%)] gap-5 m-auto justify-center">
                      <Figures
                        brandKey={secondProject}
                        currentDate={currentDate}
                        prevDate={prevDate}
                      />
                      <div className="col-span-2">
                        <div className="">
                          <SourcesChart
                            brandKey={secondProject}
                            currentDate={currentDate}
                            prevDate={prevDate}
                          />
                        </div>
                      </div>
                      <div className="col-span-2">
                        <div className="">
                          <SentimentChart
                            brandKey={brandKey}
                            currentDate={currentDate}
                            prevDate={prevDate}
                          />
                        </div>
                      </div>
                    </div>
                  </CardBody>
                </Card>
              ) : null} */}
            </>
          )}
        </div>
      )}
    </MainLayout>
  );
};

export default Comparison;
