import { useNavigate } from "react-router-dom";

export default function Filters({ open, setOpen }) {
  const navigate = useNavigate();

  return (
    <>
      <div className="flex justify-between items-center">
        <span className="font-normal text-sm text-gray-700">
          Project Comparison
        </span>
        <div className="flex items-center">
          <button
            type="button"
            className="inline-flex items-center ml-2 rounded-md border border-transparent bg-indigo-600 px-3 py-2 text-sm font-medium leading-4 text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            onClick={() => setOpen(!open)}
          >
            Compare project
          </button>
        </div>
      </div>
    </>
  );
}
