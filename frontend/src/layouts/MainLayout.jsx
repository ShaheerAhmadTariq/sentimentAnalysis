import { Footer } from "../ui/Footer/Footer";
import { Navbar } from "../ui/Navbar/Navbar";
import { Sidebar } from "../ui/Sidebar/Sidebar";
import React, { useState, useEffect } from "react";
import { Router, useNavigate } from "react-router-dom";

export const MainLayout = ({ currentProjectFetch = undefined, children }) => {
  const [showSideBar, setShowSideBar] = useState(true);
  const [IsLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  var user = JSON.parse(localStorage.getItem("userEmail"));

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
  }, []);

  // useEffect(() => {
  //   if (typeof window !== "undefined") {
  //     const userData=
  //       sessionStorage.getItem("userDataMS") ||
  //       sessionStorage.getItem("LocalUser");

  //     if (!userData) {
  //       Router.push("/");
  //     } else {
  //       setIsLoading(false);
  //     }
  //   }
  // }, []);
  return (
    <>
      <div>
        <Navbar handleSideBarStatus={() => setShowSideBar(!showSideBar)} />
        <div className="flex bg-gray-50 pt-16">
          <Sidebar
            currentProjectFetch={currentProjectFetch}
            showSideBar={showSideBar}
          />
          <div
            className={`relative h-full bg-gray-50 transition delay-150 ease-in-out ml-auto ${
              showSideBar
                ? "w-full lg:w-[calc(100%_-_16rem)]"
                : "w-full sm:w-full md:w-full lg:w-full"
            } `}
          >
            <main>{children}</main>
            <Footer />
          </div>
        </div>
      </div>
    </>
  );
};
