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
  const [days, setDays] = useState(30)

  const [newsmentions, setNewsMentions] = useState([]);
  const [redditmentions, setRedditMentions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGetting, setIsGetting] = useState(false);
  const [newsCheck, setNewsCheck] = useState(true);
  const [redditCheck, setRedditCheck] = useState(false);
  const [positiveCheck, setPositiveCheck] = useState(false);
  const [negativeCheck, setNegativeCheck] = useState(false);
  const [neutralCheck, setNeutralCheck] = useState(false);
  const [finalRecord, setFinalRecord] = useState([]);
  const [finalData, setFinalData] = useState([]);
  

  useEffect(() => {
    async function card() {
     
  // let cards = await  fetch('http://localhost:8000/cards')

  let p_id =JSON.parse( localStorage.getItem("brandList"))
  let {id} =JSON.parse( localStorage.getItem("userEmail"))
  let cards = await fetch('http://localhost:8000/cards/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({p_id: p_id[0].p_id,days,u_id:id}),
})



  cards = await cards.json()
  console.log("res",cards)
  let positive=cards[0];
  let negative=cards[1];
  let neutral=cards[2];

  positive=positive.map((elm,ind)=>{
      return {...elm,sentiment:"Positive"}
  })
  negative=negative.map((elm,ind)=>{
      return {...elm,sentiment:"Negative"}
  })
  neutral=neutral.map((elm,ind)=>{
      return {...elm,sentiment:"Neutral"}
  })

  setFinalData([...positive,...negative,...neutral])
  setFinalRecord([...positive,...negative,...neutral])



}card()},  [days]);

  const [currentPage, setCurrentPage] = useState(1);
  const [mentionsPerPage] = useState(10);

  const lastPageIndex = currentPage * mentionsPerPage;
  const firstPageIndex = lastPageIndex - mentionsPerPage;
  const currentMentions = finalData?.slice(firstPageIndex, lastPageIndex);

  var brandKey = JSON.parse(localStorage.getItem("brandList"))
  brandKey=brandKey[0].brandNames
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

  useEffect(() => {
    // getNewsMentions();
    // getRedditMentions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [brandKey]);
  // getBrandListing

  // get mentions from news api
  async function getNewsMentions() {
    setIsLoading(true);

    // encode to scape spaces
    const esc = encodeURIComponent;
    const url =
      "http://127.0.0.1:8000/sentimentGraph";
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
        setNewsMentions(data.data?.articles);
        setIsLoading(false);
      });
  }
  // get mentions from reddit api
  async function getRedditMentions() {
    setIsLoading(true);

    // encode to scape spaces
    const esc = encodeURIComponent;
    const url =
      "http://127.0.0.1:8000/sentimentGraph";
    const params = {
      keyword: brandKey,
      limit: 100,
    };
    // this line takes the params object and builds the query string
    const query = Object.keys(params)
      .map((k) => `${esc(k)}=${esc(params[k])}`)
      .join("&");

    await fetch(url + query)
      .then((res) => res.json())
      .then((data) => {
        setRedditMentions(data?.data);
      });
  }

  useEffect(() => {
    if (newsCheck) {
      setFinalRecord(newsmentions);
    } else if (redditCheck) {
      setFinalRecord(redditmentions);
    } else {
      setFinalRecord(newsmentions);
    }
  }, [newsCheck, newsmentions, redditCheck, redditmentions]);

  useEffect(() => {
    if (positiveCheck) {
      setFinalData(finalRecord.filter((p) => p.sentiment === "Positive"));
    } else if (negativeCheck) {
      setFinalData(finalRecord.filter((n) => n.sentiment === "Negative"));
    } else if (neutralCheck) {
      setFinalData(finalRecord.filter((nu) => nu.sentiment === "Neutral"));
    } else setFinalData(finalRecord);
  }, [positiveCheck, negativeCheck, neutralCheck, finalRecord]);

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
                {!redditCheck ? (
                  <SentimentGraph
                  days={days} setDays={setDays}
                    brandKey={brandKey}
                    currentDate={currentDate}
                    prevDate={prevDate}
                  />
                ) : (
                  <RedditSentiment
                    brandKey={brandKey}
                    currentDate={currentDate}
                    prevDate={prevDate}
                  />
                )}
              </div>
            </CardBody>
          </Card>
          <Card className="my-4">
            <CardBody>
              <div className="flex justify-between items-center">
                <Filter
                  newsCheck={newsCheck}
                  setNewsCheck={setNewsCheck}
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
                                    <span>{m.source?.name || m.source}</span>
                                    <time
                                      className="ml-2"
                                      dateTime={m.publishedAt}
                                    >
                                      {m.publishedAt}
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
                            <div
                              className="mt-2 space-y-4 text-sm text-gray-700"
                            />
                            {m.description.length>=176?m.description.substring(0,176):m.description}
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
