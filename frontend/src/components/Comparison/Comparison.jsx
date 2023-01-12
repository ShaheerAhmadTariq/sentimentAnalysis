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
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [data,setData]=useState(undefined)
  const [brandList, setBrandList] = useState(JSON.parse(localStorage.getItem("brandList")));
  const [secondProject, setSecondProject] = useState("");

  var brandKey = JSON.parse(localStorage.getItem("brandList"));
  // brandKey = brandKey?.at(-1).replace(/^\s+/g, "");

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

  async function getData(){
    let resp=await fetch('http://localhost:8000/CountComparison');
    resp=await resp.json();
    console.log(resp);
    // setBrandList([...brandList,...resp])
    setData(resp)
  }

console.log("BrandList", brandList)
  useEffect(()=>{
    getData();
  },[])


  return (
    <MainLayout>
      {brandList?.length > 1 ? (
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
            {/* New Comment 1 */}
              {/* <ProjectsModal
                open={open}
                setOpen={setOpen}
                brandList={brandList}
                isLoading={isLoading}
                secondProject={secondProject}
                setSecondProject={setSecondProject}
              />
              <Card className="my-4">
                <CardBody>
                  <Filters open={open} setOpen={setOpen} />
                </CardBody>
              </Card>
              <Card>
                <CardBody>
                  <div>
                    <p className="capitalize">{brandKey}</p>
                    <Graph1
                      brandKey={brandKey}
                      currentDate={currentDate}
                      prevDate={prevDate}
                    />
                  </div>
                </CardBody>
              </Card> */}
              {/* Old Comments */}
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



              {data?
              <>
              {/* Card Comments */}
              <Card className="my-4">
              <CardBody>
                <p className="capitalize">{Object.keys(data)[0]}</p>

                <div className="grid grid-cols-[repeat(auto-fit,_15.666666%)] gap-5 m-auto justify-center">
                  <Figures
                    data={data.project01}
                    brandKey={brandKey}
                    currentDate={currentDate}
                    prevDate={prevDate}
                  />
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
                  <div className="col-span-2">
                    <div className="">
                      {/* <SentimentChart
                        data={data.project01}
                        brandKey={brandKey}
                        currentDate={currentDate}
                        prevDate={prevDate}
                      /> */}
                    </div>
                  </div>
                </div>
              </CardBody>
            </Card>
              <Card className="my-4">
              <CardBody>
                <p className="capitalize">{Object.keys(data)[1]}</p>

                <div className="grid grid-cols-[repeat(auto-fit,_15.666666%)] gap-5 m-auto justify-center">
                  <Figures
                    data={data.project02}
                    brandKey={brandKey}
                    currentDate={currentDate}
                    prevDate={prevDate}
                  />
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
              :null}





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
