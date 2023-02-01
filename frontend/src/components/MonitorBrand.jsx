import { keywords } from "../assets";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader } from "../ui/Loader";
import { ToastContainer, toast } from "react-toastify";

export default function MonitorBrand() {
  const [brandKeywords, setBrandKeywords] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  var userEmail = JSON.parse(localStorage.getItem("userEmail"));
  const navigate = useNavigate();

  function handleInput(e) {
    setBrandKeywords(e.target.value);
  }

  function splitKeywords(brandKeywords) {
    let keywords = brandKeywords.split(",");
    if (keywords.length === 1) {
      keywords = [...keywords, "null", "null"];
    } else if (keywords.length === 2) {
      keywords = [...keywords, "null"];
    }
    return keywords.join(",");
  }

  async function createBrand(e) {
    e.preventDefault();
    let brandKeywordsArray = splitKeywords(brandKeywords);
    setIsLoading(true);
    try {
      await fetch("http://127.0.0.1:8000/createProject", {
        method: "POST",
        body: JSON.stringify({
          enterBrandCompetitorHashtag: brandKeywordsArray,
          email: userEmail,
        }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("res", data);

          if (data.message === "Success") {
            console.log(data);
            setIsLoading(false);
            localStorage.setItem(
              "brandList",
              JSON.stringify([
                { p_id: data.p_id, brandNames: brandKeywordsArray.split(",") },
              ])
            );
            

            navigate("/mentions");
          } else {
            toast.error(data.message);
            setIsLoading(false);
          }
        });
    } catch (err) {
      console.log(err);
    }
  }
  return (
    <>
      <div className="flex min-h-screen">
        <div className="flex flex-1 flex-col mt-28 px-6">
          <div className="w-full">
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-gray-900">
                Enter Keywords
              </h2>
              <p className="mt-2 text-sm text-indigo-600">
                Enter brand, competitor or hashtag to monitor
              </p>
            </div>

            <div className="mt-6">
              <form className="space-y-6" onSubmit={createBrand}>
                <div>
                  <div className="mt-1">
                    <input
                      id="keywords"
                      name="keywords"
                      type="text"
                      autoComplete="keywords"
                      required
                      placeholder="e.g Pepsi, Sprite, Pepsi"
                      className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                      onChange={handleInput}
                    />
                  </div>
                  <p className="mt-2 mb-8 text-sm text-gray-500">
                    Type comma separated phrases to monitor
                  </p>
                </div>
                <hr />

                <div>
                  {isLoading ? (
                    <div className="flex flex-col justify-center items-center">
                      <h5>Creating Brand! This may take a while.</h5>
                      <Loader center className="text-indigo-600 mt-3" />
                    </div>
                  ) : (
                    <button className="float-right rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                      Next
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="relative hidden w-0 flex-1 lg:block">
          <img
            className="absolute inset-0 h-full w-full object-cover"
            src={keywords}
            alt=""
          />
        </div>
      </div>
      <ToastContainer />
    </>
  );
}
