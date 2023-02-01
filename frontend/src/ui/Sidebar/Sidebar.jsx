import {
  HomeIcon,
  // StarIcon,
  ChatBubbleOvalLeftIcon,
  ChartPieIcon,
  DocumentIcon,
} from "@heroicons/react/24/solid";
import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";

let iconClass =
  "h-6 w-6 flex-shrink-0 text-gray-500 transition duration-75 group-hover:text-gray-900";

const sideNavigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: <HomeIcon className={iconClass} />,
  },

  {
    name: "Mentions",
    href: "/mentions",
    icon: <ChatBubbleOvalLeftIcon className={iconClass} />,
  },
  {
    name: "Comparison",
    href: "/comparison",
    icon: <ChartPieIcon className={iconClass} />,
  },
  {
    name: "Reports",
    href: "/report",
    icon: <DocumentIcon className={iconClass} />,
  },
];

export const Sidebar = ({ currentProjectFetch = undefined, showSideBar }) => {
  const [brandKey, setbrandKey] = useState([]);
  const [brandKeys, setbrandKeys] = useState([]);
  useEffect(() => {
    if (currentProjectFetch?.projectFetch) {
      setbrandKey(currentProjectFetch?.currentProject?.brandNames?.at(-1));
      setbrandKeys(currentProjectFetch?.currentProject?.brandNames);
    } else {
      var brandKey = JSON.parse(localStorage.getItem("brandList"));
      var brandKeys = JSON.parse(localStorage.getItem("brandList"));
      brandKey = brandKey ? brandKey[0].brandNames : null;
      brandKeys = brandKeys ? brandKeys[0]?.brandNames : [];
      brandKey = brandKey?.at(-1);

      setbrandKey(brandKey);
      setbrandKeys(brandKeys);
    }
  }, [currentProjectFetch]);

  return (
    <aside
      id="sidebar"
      className={`fixed top-0 left-0 z-20 h-full flex-shrink-0 flex-col pt-16 transition-width duration-75 sm:w-0 flex lg:w-64 ${
        !showSideBar && "w-0 sm:w-0 lg:-w-64"
          ? "w-64 sm:w-64 md:w-64 lg:w-0"
          : "w-0"
      }  `}
    >
      <div className="relative flex min-h-0 flex-1 flex-col border-r border-gray-200 bg-white pt-0">
        <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
          <div className="flex-1 space-y-1 divide-y divide-gray-200 bg-white px-3">
            <ul className="space-y-2">
              {brandKey && (
                <NavLink
                  to="/mentions"
                  className="flex border-l-4 border-0 rounded-none border-lime-600 cursor-pointer items-center p-2 text-base font-normal text-gray-900"
                >
                  <span
                    className="ml-3 flex-1 capitalize whitespace-nowrap"
                    data-testid="sidebar-item-content"
                  >
                    {brandKey ? brandKey : "APSS"}
                  </span>
                  <div className="flex-shrink-0 w-2 h-2 rounded-full bg-lime-600"></div>
                </NavLink>
              )}
              {sideNavigation.map((item) => (
                <NavLink
                  to={item.href}
                  key={item.name}
                  className={({ isActive }) =>
                    isActive
                      ? "flex cursor-pointer items-center rounded-lg p-2 text-base font-normal text-gray-900 bg-gray-100 "
                      : "flex cursor-pointer items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-gray-100"
                  }
                >
                  {item.icon}
                  <span
                    className="ml-3 flex-1 whitespace-nowrap"
                    data-testid="sidebar-item-content"
                  >
                    {item.name}
                  </span>
                </NavLink>
              ))}
              <hr />
              {brandKeys &&
                brandKeys?.map((item, idx) => (
                  <NavLink
                    to="/mentions"
                    key={idx}
                    className="flex cursor-pointer items-center rounded-lg p-2 text-base font-normal text-gray-900 capitalize bg-gray-100"
                  >
                    {item}
                  </NavLink>
                ))}
            </ul>
          </div>
        </div>
      </div>
    </aside>
  );
};
