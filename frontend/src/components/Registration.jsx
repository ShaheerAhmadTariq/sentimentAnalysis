import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Capture  from "../assets/Capture.PNG";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Loader } from "../ui/Loader";
import { useNavigate } from "react-router-dom";

export default function Registration() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [termsCheck, setTermsCheck] = useState(false);

  const navigate = useNavigate();

  var user = JSON.parse(localStorage.getItem("userEmail"));

  useEffect(() => {
    if (user) {
      navigate("/mentions");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function signUp(e) {
    if( /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(email))
    {
      console.log("valid email")
    
    e.preventDefault();

    setIsLoading(true);

    let values = { username, email, password };

    try {
      await fetch("http://127.0.0.1:8000/users", {
        method: "POST",
        body: JSON.stringify(values),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message === "Successfully created user.") {
            toast.success("You are successfully registered!");
            localStorage.setItem(
              "userEmail",
              JSON.stringify({
                email: data.user_email,
                id: data.user_id,
                username: data.username,
              })
            );
            setTimeout(() => {
              navigate("/monitor");
            }, 1500);
          } else {
            toast.error(data.message);
          }
          setIsLoading(false);
        });
    } catch (err) {
      console.log(err);
    }
    }
    else{
      alert('Enter Valid Email Address')
    }
  }
  return (
    <>
      <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <img className="mx-auto h-28 w-auto" src={Capture} alt="Your Company" />
          <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">
            Create your account
          </h2>
          
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form className="space-y-6" onSubmit={signUp}>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
                  Username
                </label>
                <div className="mt-1">
                  <input
                    id="username"
                    name="text"
                    type="text"
                    required
                    value={username}
                    className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
              </div>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
                  Email address
                </label>
                <div className="mt-1">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={email}
                    className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700"
                >
                  Password
                </label>
                <div className="mt-1">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    pattern="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
                    title="Minimum eight characters, at least one letter, one number and one special character"
                    onChange={(e) => setPassword(e.target.value)}
                    value={password}
                    className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                {isLoading ? (
                  <Loader center className="text-indigo-600" />
                ) : (
                  <button
                    className="flex disabled:cursor-not-allowed disabled:hover:bg-gray-500 w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    disabled={termsCheck ? false : true}
                  >
                    Sign up
                  </button>
                )}
              </div>

              <div className="flex">
                <p className="text-center text-sm text-gray-600">
                  Already a user?{" "}
                  <Link
                    to="/login"
                    className="font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    Log in
                  </Link>
                </p>
              </div>

              <div className="flex">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  checked={termsCheck}
                  onChange={() => setTermsCheck((prev) => !prev)}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label
                  htmlFor="remember-me"
                  className="ml-2 block text-xs text-gray-900"
                >
                  By signing up I agree to the terms & conditions and privacy
                  policy.
                </label>
              </div>
            </form>
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
}
