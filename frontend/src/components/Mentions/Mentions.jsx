import React from "react";
import { useState, useEffect } from "react";
import { MainLayout } from "../../layouts/MainLayout";
import { Card, CardBody } from "../../ui/Card";
import Filter from "./Filter";
import SentimentGraph from "./SentimentGraph";
import RedditSentiment from "./RedditSentiment";
import { Link } from "react-router-dom";

import {
  // TagIcon,
  // TrashIcon,
  BoltIcon,
  // PlusCircleIcon,
} from "@heroicons/react/20/solid";
import { Loader } from "../../ui/Loader";
import { reddit } from "../../assets";

const Mentions = () => {
  const [days, setDays] = useState(30);

  const [isLoading, setIsLoading] = useState(false);
  const [isGetting, setIsGetting] = useState(false);
  const [newsCheck, setNewsCheck] = useState(false);
  const [search, setsearch] = useState("");
  const [redditCheck, setRedditCheck] = useState(false);
  const [allCheck, setallCheck] = useState(true);
  const [positiveCheck, setPositiveCheck] = useState(false);
  const [negativeCheck, setNegativeCheck] = useState(false);
  const [neutralCheck, setNeutralCheck] = useState(false);
  const [finalRecord, setFinalRecord] = useState([]);
  const [finalData, setFinalData] = useState([]);
  const [multiGraph, setmultiGraph] = useState(true);

  useEffect(() => {
    async function card() {
      // let cards = await  fetch('http://localhost:8000/cards')

      let brandList = JSON.parse(localStorage.getItem("brandList"));
      const p_id = brandList[0]?.p_id;
      let { id } = JSON.parse(localStorage.getItem("userEmail"));
      if (!id || !p_id) {
        alert("No user id or product id found");
        return;
      }
      let cards = await fetch("http://localhost:8000/cards/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ p_id, days, u_id: id , days: 3000}),
      });
      cards = await cards.json();

      let positiveNewsApi = cards["NewsApi"][0].map((elm, ind) => {
        return { ...elm, sentiment: "Positive", source: "News" };
      });
      let negativeNewsApi = cards["NewsApi"][1].map((elm, ind) => {
        return { ...elm, sentiment: "Negative", source: "News" };
      });
      let neutralNewsApi = cards["NewsApi"][2].map((elm, ind) => {
        return { ...elm, sentiment: "Neutral", source: "News" };
      });

      let positiveReddit = cards["Reddit"][0].map((elm, ind) => {
        return { ...elm, sentiment: "Positive", source: "Reddit" };
      });
      let negativeReddit = cards["Reddit"][1].map((elm, ind) => {
        return { ...elm, sentiment: "Negative", source: "Reddit" };
      });
      let neutralReddit = cards["Reddit"][2].map((elm, ind) => {
        return { ...elm, sentiment: "Neutral", source: "Reddit" };
      });

      const finalData = [
        ...positiveNewsApi,
        ...positiveReddit,
        ...negativeNewsApi,
        ...negativeReddit,
        ...neutralNewsApi,
        ...neutralReddit,
      ];
      setFinalData(finalData);
      setFinalRecord(finalData);
    }
    card();
  }, [days]);

  const [currentPage, setCurrentPage] = useState(1);
  const [mentionsPerPage] = useState(10);

  const lastPageIndex = currentPage * mentionsPerPage;
  const firstPageIndex = lastPageIndex - mentionsPerPage;
  const currentMentions = finalData?.slice(firstPageIndex, lastPageIndex);

  var brandKey = JSON.parse(localStorage.getItem("brandList"));
  brandKey = brandKey[0].brandNames;
  brandKey = brandKey?.at(-1);

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

  const filterCards = () => {
    if (finalRecord.length > 0) {
      let filteredRecord = finalRecord;
      if (newsCheck) {
        filteredRecord = filteredRecord.filter((p) => p.source === "News");
      }
      if (redditCheck) {
        filteredRecord = filteredRecord.filter((p) => p.source === "Reddit");
      }
      if (positiveCheck) {
        filteredRecord = filteredRecord.filter(
          (p) => p.sentiment === "Positive"
        );
      }
      if (negativeCheck) {
        filteredRecord = filteredRecord.filter(
          (n) => n.sentiment === "Negative"
        );
      }
      if (neutralCheck) {
        filteredRecord = filteredRecord.filter(
          (nu) => nu.sentiment === "Neutral"
        );
      }
      if (search) {
        filteredRecord = filteredRecord.filter((item) =>
          item?.author?.toLowerCase()?.includes(search.toLowerCase())
        );
      }
      setCurrentPage(1)
      setFinalData(filteredRecord);
    }
  };

  useEffect(() => {
    filterCards();
  }, [
    newsCheck,
    redditCheck,
    allCheck,
    positiveCheck,
    negativeCheck,
    neutralCheck,
    search,
    finalRecord,
  ]);

  useEffect(() => {
    setIsGetting(true);
    if (brandKey) {
      setIsGetting(false);
    } else {
      setIsGetting(true);
    }
  }, [brandKey]);

  return (
    <MainLayout>
      {brandKey ? (
        <div className="m-4 min-h-screen">
          <Card>
            <CardBody>
              <div>
                <button className="text-gray-500 text-sm">
                  Show Sentiment
                </button>
                {/* Graph */}
                <div className="flex space-x-2 items-center">
                  <label className="text-sm">
                    {multiGraph ? "Multi Graph" : "Single Graph"}
                  </label>
                  <input
                    type="checkbox"
                    checked={multiGraph}
                    onChange={(e) => setmultiGraph(!multiGraph)}
                  />
                </div>

                <SentimentGraph
                  days={days}
                  setDays={setDays}
                  brandKey={brandKey}
                  currentDate={currentDate}
                  prevDate={prevDate}
                  multiGraph={multiGraph}
                />
              </div>
            </CardBody>
          </Card>
          <Card className="my-4">
            <CardBody>
              <div className="flex justify-between items-center">
                {/* Checkboxes and pagination filter */}
                <Filter
                  allCheck={allCheck}
                  setAllCheck={setallCheck}
                  newsCheck={newsCheck}
                  setNewsCheck={setNewsCheck}
                  search={search}
                  setSearch={setsearch}
                  redditCheck={redditCheck}
                  setRedditCheck={setRedditCheck}
                  totalMentions={finalData?.length}
                  mentionsPerPage={mentionsPerPage}
                  setCurrentPage={setCurrentPage}
                  currentPage={currentPage}
                />
              </div>
            </CardBody>
          </Card>

          {isLoading ? (
            <Loader className="text-indigo-600" />
          ) : (
            // Mention Cards
            <div className="flex justify-between gap-4">
              <ul className="overflow-y-scroll h-[calc(100vh_-_10vh)]">
                {currentMentions &&
                  currentMentions.map((m, idx) => (
                    <Card className="mb-4" key={idx}>
                      <CardBody>
                        <li>
                          <article>
                            <div>
                              <div className="flex space-x-3">
                                {redditCheck ? (
                                  <img
                                    className="h-10 w-10 rounded-full"
                                    src={reddit}
                                    alt=""
                                  />
                                ) : m.urlToImage ? (
                                  <img
                                    className="h-10 w-10 rounded-full"
                                    src={m.urlToImage}
                                    alt=""
                                  />
                                ) : (
                                  <div className="h-10 w-10 rounded-full bg-black"></div>
                                )}

                                <div className="min-w-0 flex-1">
                                  <p className="text-sm flex justify-between font-medium text-gray-900">
                                    {m.author ? (
                                      <span>
                                        {m.author?.length > 100
                                          ? `${m.author.substring(0, 70)}...`
                                          : m.author}
                                      </span>
                                    ) : (
                                      <span>Author</span>
                                    )}
                                    <span
                                      className={
                                        m.sentiment === "Negative"
                                          ? "bg-red-500 rounded-full px-3 py-1 text-white"
                                          : m.sentiment === "Positive"
                                          ? "bg-green-500 rounded-full px-3 py-1 text-white"
                                          : "bg-indigo-600 text-white rounded-full px-3 py-1"
                                      }
                                    >
                                      {m.sentiment}
                                    </span>
                                  </p>
                                  <p className="text-sm text-gray-500">
                                    <span className="rounded-full px-2 py-1 bg-[#282828] text-white">
                                      {m.source?.name || m.source}
                                    </span>
                                    <time
                                      className="ml-2"
                                      dateTime={m.published_at}
                                    >
                                      {m.published_at}
                                    </time>
                                  </p>
                                </div>
                              </div>
                              <h2 className="mt-4 text-base font-medium text-gray-900">
                                <a
                                  href={m.url}
                                  className="hover:underline cursor-pointer"
                                >
                                  {m.title}
                                </a>
                              </h2>
                            </div>
                            <div className="mt-2 space-y-4 text-sm text-gray-700" />
                            {m.description.length >= 176
                              ? m.description.substring(0, 176)
                              : m.description}
                            <div className="mt-6 flex justify-between space-x-8">
                              <div className="flex space-x-6">
                                <span className="inline-flex items-center text-sm">
                                  <button
                                    type="button"
                                    className="inline-flex space-x-2 text-gray-400 hover:text-gray-500"
                                  >
                                    <BoltIcon
                                      className="h-5 w-5"
                                      aria-hidden="true"
                                    />
                                    <a
                                      href={m.url}
                                      className="font-medium text-gray-900"
                                    >
                                      Visit
                                    </a>
                                  </button>
                                </span>
                                {/* <span className="inline-flex items-center text-sm">
                                  <button
                                    type="button"
                                    className="inline-flex space-x-2 text-gray-400 hover:text-gray-500"
                                  >
                                    <TagIcon
                                      className="h-5 w-5"
                                      aria-hidden="true"
                                    />
                                    <span className="font-medium text-gray-900">
                                      Tags
                                    </span>
                                  </button>
                                </span> */}
                                {/* <span className="inline-flex items-center text-sm">
                                  <button
                                    type="button"
                                    className="inline-flex space-x-2 text-gray-400 hover:text-gray-500"
                                  >
                                    <TrashIcon
                                      className="h-5 w-5"
                                      aria-hidden="true"
                                    />
                                    <span className="font-medium text-gray-900">
                                      Delete
                                    </span>
                                  </button>
                                </span> */}
                                {/* <span className="inline-flex items-center text-sm">
                                  <button
                                    type="button"
                                    className="inline-flex space-x-2 text-gray-400 hover:text-gray-500"
                                  >
                                    <PlusCircleIcon
                                      className="h-5 w-5"
                                      aria-hidden="true"
                                    />
                                    <span className="font-medium text-gray-900">
                                      Add to pdf report
                                    </span>
                                  </button>
                                </span> */}
                              </div>
                            </div>
                          </article>
                        </li>
                      </CardBody>
                    </Card>
                  ))}
              </ul>
              {/* side filter */}
              <div className="self-start">
                <Card>
                  <CardBody>
                    <h3>Sentiment:</h3>
                    <div className="flex justify-between mt-4 gap-2">
                      <div className="relative flex items-start">
                        <div className="flex h-5 items-center">
                          <input
                            id="positve"
                            aria-describedby="positve-description"
                            name="positve"
                            type="checkbox"
                            checked={positiveCheck}
                            onChange={() => {
                              setPositiveCheck((prev) => !prev);
                              setNegativeCheck(false);
                              setNeutralCheck(false);
                            }}
                            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </div>
                        <div className="ml-2 text-sm">
                          <label
                            htmlFor="positive"
                            className="font-medium text-green-500"
                          >
                            Positive
                          </label>
                        </div>
                      </div>

                      <div className="relative flex items-start">
                        <div className="flex h-5 items-center">
                          <input
                            id="negative"
                            aria-describedby="negative-description"
                            name="negative"
                            type="checkbox"
                            checked={negativeCheck}
                            onChange={() => {
                              setNegativeCheck((prev) => !prev);
                              setPositiveCheck(false);
                              setNeutralCheck(false);
                            }}
                            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </div>
                        <div className="ml-2 text-sm">
                          <label
                            htmlFor="negative"
                            className="font-medium text-red-500"
                          >
                            Negative
                          </label>
                        </div>
                      </div>

                      {/* neutral */}
                      <div className="relative flex items-start">
                        <div className="flex h-5 items-center">
                          <input
                            id="neutral"
                            aria-describedby="neutral-description"
                            name="neutral"
                            type="checkbox"
                            checked={neutralCheck}
                            onChange={() => {
                              setNeutralCheck((prev) => !prev);
                              setPositiveCheck(false);
                              setNegativeCheck(false);
                            }}
                            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                          />
                        </div>
                        <div className="ml-2 text-sm">
                          <label
                            htmlFor="neutral"
                            className="font-medium text-gray-700"
                          >
                            Neutral
                          </label>
                        </div>
                      </div>
                    </div>
                  </CardBody>
                </Card>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="m-4 min-h-screen">
          {!isGetting ? (
            <>
              <Card>
                <CardBody>
                  You don't have any project yet!
                  <Link to="/monitor">
                    <button
                      type="button"
                      className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-3 py-2 text-sm font-medium leading-4 text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    >
                      Create One
                    </button>
                  </Link>
                </CardBody>
              </Card>
            </>
          ) : (
            <Loader className="text-indigo-600" />
          )}
        </div>
      )}
    </MainLayout>
  );
};

export default Mentions;
