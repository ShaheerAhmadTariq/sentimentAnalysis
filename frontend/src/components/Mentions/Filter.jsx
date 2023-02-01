import {
  ArrowLongLeftIcon,
  ArrowLongRightIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/20/solid";
export default function Filter({
  newsCheck,
  setNewsCheck,
  redditCheck,
  setRedditCheck,
  totalMentions,
  mentionsPerPage,
  setCurrentPage,
  currentPage,
  search,
  setSearch,
  allCheck,
  setAllCheck,
}) {
  var pages = [];

  for (let i = 1; i <= Math.ceil(totalMentions / mentionsPerPage); i++) {
    pages.push(i);
  }

  return (
    <div className="flex flex-col items-start space-y-3">
      <div className="flex flex-col md:flex-row items-center justify-between space-y-10 md:space-y-0 md:space-x-10">
        {/* Checkboxes */}
        <div className="flex">
          <div className="relative flex items-start">
            <div className="flex h-5 items-center">
              <input
                id="comments"
                aria-describedby="comments-description"
                name="comments"
                checked={allCheck}
                onChange={() => {
                  setNewsCheck(false);
                  setRedditCheck(false);
                  setAllCheck(true);
                }}
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
            </div>
            <div className="ml-2 text-sm">
              <label htmlFor="comments" className="font-medium text-gray-700">
                All
              </label>
            </div>
          </div>
          <div className="relative ml-5 flex items-start">
            <div className="flex h-5 items-center">
              <input
                id="comments"
                aria-describedby="comments-description"
                name="comments"
                type="checkbox"
                checked={newsCheck}
                onChange={() => {
                  setNewsCheck(true);
                  setRedditCheck(false);
                  setAllCheck(false);
                }}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
            </div>
            <div className="ml-2 text-sm">
              <label htmlFor="comments" className="font-medium text-gray-700">
                News
              </label>
            </div>
          </div>
          <div className="relative ml-5 flex items-start">
            <div className="flex h-5 items-center">
              <input
                id="comments"
                aria-describedby="comments-description"
                name="comments"
                type="checkbox"
                checked={redditCheck}
                onChange={() => {
                  setRedditCheck(true);
                  setNewsCheck(false);
                  setAllCheck(false);
                }}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
            </div>
            <div className="ml-2 text-sm">
              <label htmlFor="comments" className="font-medium text-gray-700">
                Reddit
              </label>
            </div>
          </div>
        </div>

        {/* Search */}
        <div className=" flex items-center space-x-2">
          <input
            type="text"
            className="rounded-md flex-1 "
            placeholder="Search By Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <MagnifyingGlassIcon className="w-6 h-6 cursor-pointer" />
        </div>
      </div>

      {/* pagination */}
      <div className="w-1/2">
        <nav className="flex items-center justify-between border-t border-gray-200 px-4 sm:px-0 overflow-x-scroll">
          <div className="-mt-px flex w-0 flex-1">
            <span className="inline-flex cursor-pointer items-center border-t-2 border-transparent pt-4 pr-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700">
              <ArrowLongLeftIcon
                className={
                  currentPage === 1 ? "hidden" : "mr-3 h-5 w-5 text-gray-400"
                }
                aria-hidden="true"
                onClick={() => setCurrentPage(currentPage - 1)}
              />
            </span>
          </div>
          <div className="hidden md:-mt-px md:flex">
            {pages.map((page, idx) => (
              <span
                key={idx}
                className={
                  page === currentPage
                    ? "inline-flex cursor-pointer items-center border-t-2 border-indigo-500 px-4 pt-4 text-sm font-medium text-indigo-600"
                    : "inline-flex items-center cursor-pointer border-t-2 border-transparent px-4 pt-4 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
                }
                onClick={() => setCurrentPage(page)}
              >
                {page}
              </span>
            ))}
            {/* Current: "border-indigo-500 text-indigo-600", Default: "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300" */}
          </div>
          <div className="-mt-px flex w-0 flex-1 justify-end">
            <span className="inline-flex cursor-pointer items-center border-t-2 border-transparent pt-4 pl-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700">
              <ArrowLongRightIcon
                className={
                  currentPage === pages.length
                    ? "hidden"
                    : "ml-3 h-5 w-5 text-gray-400"
                }
                aria-hidden="true"
                onClick={() => setCurrentPage(currentPage + 1)}
              />
            </span>
          </div>
        </nav>
      </div>
    </div>
  );
}
