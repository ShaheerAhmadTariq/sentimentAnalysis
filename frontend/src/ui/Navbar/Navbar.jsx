import SidebarMobileHamburger from "../../icons/SidebarMobileHamburger";
import SidebarMobileClose from "../../icons/SidebarMobileClose";
import { useState } from "react";
import React from "react";
import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

export const Navbar = ({ handleSideBarStatus }) => {
  const [isActive, setActive] = useState(false);
  const [username, setUsername] = useState("");

  const navigate = useNavigate();

  const toggleClass = () => {
    setActive(!isActive);
  };

  const SignoutButton = () => {
    return (
      <a
        href="#/"
        className="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
        onClick={() => {
          localStorage.clear();
          navigate("/login");
        }}
        role="menuitem"
      >
        LogOut
      </a>
    );
  };
  const toggleSidebar = () => {
    handleSideBarStatus();
  };

  useEffect(() => {
    const users = JSON.parse(localStorage.getItem("userEmail"));
    if (users) {
      setUsername(users.username);
    }
  }, []);

  return (
    <>
      <nav className="fixed z-30 w-full border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
        <div className="py-3 px-3 lg:px-5 lg:pl-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <button
                id="toggleSidebar"
                aria-expanded="true"
                aria-controls="sidebar"
                onClick={toggleSidebar}
                className="mr-3 hidden cursor-pointer rounded p-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white lg:inline"
              >
                <svg
                  className="h-6 w-6"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fillRule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clipRule="evenodd"
                  ></path>
                </svg>
              </button>
              <button
                id="toggleSidebarMobile"
                aria-expanded="true"
                aria-controls="sidebar"
                onClick={toggleSidebar}
                className="mr-2 cursor-pointer rounded p-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900 focus:bg-gray-100 focus:ring-2 focus:ring-gray-100 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white dark:focus:bg-gray-700 dark:focus:ring-gray-700 lg:hidden"
              >
                <SidebarMobileHamburger />
                <SidebarMobileClose />
              </button>
              <a href="/" className="lg:mr-14">
                APSS
              </a>
            </div>
            <div className="flex items-center">
              <p className="font-semibold flex items-center space-x-4 px-4">
                <Link to={"/aboutus"}>About Us</Link>
                <Link to="/contactus">Contact Us</Link>
              </p>
              <p className="mr-2 hidden text-sm font-normal lg:block">
                Good Morning,
                <span className="ml-1 font-semibold">{username}</span>
              </p>

              <div className="ml-3 flex flex-none items-center">
                <div>
                  <button
                    type="button"
                    className="flex rounded-full bg-gray-800 text-sm focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                    id="user-menu-button-2"
                    aria-expanded="false"
                    data-dropdown-toggle="dropdown-2"
                    onClick={toggleClass}
                  >
                    <span className="sr-only">Open user menu</span>
                    <div className="flex-shrink-0 h-8 w-8 rounded-full bg-black"></div>
                  </button>
                </div>
                <div
                  className={`absolute top-8 right-5 z-50 my-4 list-none divide-y divide-gray-100 rounded bg-white text-base shadow dark:divide-gray-600 dark:bg-gray-700 ${
                    isActive ? "" : "hidden"
                  }`}
                  id="dropdown-2"
                >
                  <ul className="py-1" role="none">
                    {/* <li>
                      <a
                        href="#/"
                        className="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                        role="menuitem"
                      >
                        Dashboard
                      </a>
                    </li> */}

                    <li>
                      <SignoutButton />
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
};
