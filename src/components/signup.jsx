import { useState, useEffect, useContext } from "react";
// import { appContext } from "../context";
// import AuthServices from "../services/AuthServices";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  let navigate = useNavigate();
  // const { setUser, setToken } = useContext(appContext);
  // const [load, setLoad] = useState(false);
  // const [status, setStatus] = useState();
  // const [authEmail, setAuthEmail] = useState();
  // const [tempToken, setTempToken] = useState();
  // const [otpJson, setOtpJson] = useState("");
  const [json, setJson] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    setJson({ ...json, [name]: value });
  };

  const handleClick = async (e) => {
    console.log("signuped");
    navigate('/user');
    localStorage.setItem("appUser", e);
    localStorage.setItem("isAuthorized", true);
    // setLoad(true);
    // await AuthServices.signup(json).then((res) => {
    //   setLoad(false);
    //   setStatus(res.status);
    //   setTempToken(res.data.data.token);
    //   setAuthEmail(res.data.data.authEmailId);
    //   console.log(res);
    // });
  };
  
  
  // const handleOTPClick = async () => {
  //   setLoad(true);
  //   const payload = {
  //     emailOtp: otpJson,
  //     authEmailId: authEmail,
  //   };
  //   await AuthServices.verifyOTP(payload, tempToken).then((res) => {
  //     console.log(res);
  //     setToken(res.data.data.token);
  //     localStorage.setItem("appToken", res.data.data.token);
  //     setUser(res.data.data.user);
  //     localStorage.setItem("appUser", JSON.stringify(res.data.data.user));
  //     localStorage.setItem("isAuthorized", true);
  //     navigate('/committee');
  //   });
  // };

  useEffect(() => {
    if(localStorage.getItem('isAuthorized')){
      navigate('/user')
    }
  }, [navigate])
  
  // console.log(otpJson);
  return (
    <>
      <div className=" w-full grid grid-flow-col grid-cols-2 min-h-screen ">
        <div className="w-full col-span-1 border border-gray-300">
          <img
            src="https://plus.unsplash.com/premium_photo-1663013172198-2cf882b7d10e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
            alt=""
            className="h-full w-full object-cover object-center lg:h-full lg:w-full"
          />
        </div>

        <div className="w-full col-span-1">
          <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="w-full max-w-md space-y-8">
              <div>
                {/* <img
                  className="mx-auto h-12 w-auto"
                  src="https://tailwindui.com/img/logos/mark.svg?color=orange&shade=600"
                  alt="Your Company"
                /> */}
                <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                  Sign up your account
                </h2>
                <p className="mt-2 text-center text-sm text-gray-600">
                  or{" "}
                  <a
                    href="/login"
                    className="font-medium text-orange-600 hover:text-orange-500"
                  >
                    Sign In
                  </a>
                </p>
              </div>
              {/* {status === 201 ? (
                <>
                  <div>
                    <label htmlFor="name" className="sr-only">
                      Enter OTP
                    </label>
                    <input
                      name="emailOtp"
                      type="number"
                      autoComplete=""
                      required
                      className="relative block w-full rounded-md my-4  border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-orange-500 focus:outline-none focus:ring-orange-500 sm:text-sm"
                      placeholder="Enter OTP"
                      onChange={(e) => setOtpJson(e.target.value)}
                    />
                  </div>
                  <button
                    type="button"
                    onClick={handleOTPClick}
                    className="group relative flex w-full justify-center rounded-md border border-transparent bg-orange-600 py-2 px-4 text-sm font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                  >
                    Verify
                  </button>
                </>
              ) : ( */}
                <>
                  <form className="mt-8 space-y-6" action="#" method="POST">
                    <input type="hidden" name="remember" defaultValue="true" />
                    <div className="-space-y-px rounded-md shadow-sm">
                      <div>
                        <label htmlFor="name" className="sr-only">
                          Name
                        </label>
                        <input
                          name="name"
                          type="text"
                          autoComplete="name"
                          required
                          className="relative block w-full rounded-md my-4  border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-orange-500 focus:outline-none focus:ring-orange-500 sm:text-sm"
                          placeholder="Name"
                          onChange={handleChange}
                        />
                      </div>
                      {/* <div>
                    <label htmlFor="number" className="sr-only">
                      Phone Number
                    </label>
                    <input
                      id="email-address"
                      name="number"
                      type="number"
                      autoComplete="number"
                      required
                      className="relative block w-full rounded-md my-4  border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-orange-500 focus:outline-none focus:ring-orange-500 sm:text-sm"
                      placeholder="Phone"
                    />
                  </div> */}
                      <div>
                        <label htmlFor="email-address" className="sr-only">
                          Email address
                        </label>
                        <input
                          name="email"
                          type="email"
                          autoComplete="email"
                          required
                          className="relative block w-full rounded-md my-4  border border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-orange-500 focus:outline-none focus:ring-orange-500 sm:text-sm"
                          placeholder="Email address"
                          onChange={handleChange}
                        />
                      </div>
                      <div>
                        <label htmlFor="password" className="sr-only">
                          Password
                        </label>
                        <input
                          name="password"
                          type="password"
                          autoComplete="current-password"
                          required
                          className="relative block w-full border rounded-md my-4 border-gray-300 px-3 py-3 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-orange-500 focus:outline-none focus:ring-orange-500 sm:text-sm"
                          placeholder="Password"
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                    <div>
                      <button
                        type="button"
                        onClick={handleClick}
                        className="group relative flex w-full justify-center rounded-md border border-transparent bg-orange-600 py-2 px-4 text-sm font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                      >
                        Sign Up
                      </button>
                    </div>
                  </form>
                </>
              {/* ) */}
              {/* } */}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
