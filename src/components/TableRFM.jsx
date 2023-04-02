import React, { useState, useEffect } from "react";
import ApiService from "../services/api";

function TableRFM() {
  const [res1, setRes1] = useState([]);
  useEffect(()=>{
    console.log("here");
    ApiService.get("http://127.0.0.1:8000/api/get_rfm").then((res) => {
        console.log(res)
      setRes1(res);
      console.log(res1);
      console.log("there");
  })},
    []
  );
  return (
    <div>
      <hr></hr>
      <section class="text-gray-600 body-font">
        <div class="container px-5 pt-4 pb-24 mx-auto">
          <div class="flex flex-col text-center w-full my-10">
            <h1 class="sm:text-4xl text-3xl font-medium title-font mb-2 text-gray-900">
              Pricing
            </h1>
            <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
              Banh mi cornhole echo park skateboard authentic crucifix neutra
              tilde lyft biodiesel artisan direct trade mumblecore 3 wolf moon
              twee
            </p>
          </div>
          <div class="lg:w-2/3 w-full mx-auto overflow-auto">
            <table class="table-auto w-full text-left whitespace-no-wrap">
              <thead>
                <tr>
                  <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-300 rounded-tl rounded-bl">
                    #
                  </th>
                  <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-300">
                    Recency
                  </th>
                  <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-300">
                    Frequency
                  </th>
                  <th class="px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-300">
                    Monetary
                  </th>
                  {/* <th class="w-10 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-300 rounded-tr rounded-br"></th> */}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="px-4 py-3">Premium</td>
                  {/* <td class="px-4 py-3">{res.data.data[0]}</td> */}
                  <td class="px-4 py-3">{res1[0][0]}</td>
                  <td class="px-4 py-3">{res1[1][0]}</td>
                  <td class="px-4 py-3 text-lg text-gray-900">{res1[2][0]}</td>
                  {/* <td class="w-10 text-center">
                    <input name="plan" type="radio" />
                  </td> */}
                </tr>
                <tr>
                  <td class="border-t-2 border-gray-300 px-4 py-3">Mediocre</td>
                  <td class="border-t-2 border-gray-300 px-4 py-3">
                    {res1}
                  </td>
                  <td class="border-t-2 border-gray-300 px-4 py-3">
                   { res1}
                  </td>
                  <td class="border-t-2 border-gray-300 px-4 py-3 text-lg text-gray-900">
                    {res1}
                  </td>
                  {/* <td class="border-t-2 border-gray-300 w-10 text-center">
                    <input name="plan" type="radio" />
                  </td> */}
                </tr>
                <tr>
                  <td class="border-t-2 border-gray-300 px-4 py-3">
                    Lower order
                  </td>
                  <td class="border-t-2 border-gray-300 px-4 py-3">
                    {res1}
                  </td>
                  <td class="border-t-2 border-gray-300 px-4 py-3">
                    {res1}
                  </td>
                  <td class="border-t-2 border-gray-300 px-4 py-3 text-lg text-gray-900">
                    {res1}
                  </td>
                  {/* <td class="border-t-2 border-gray-300 w-10 text-center">
                    <input name="plan" type="radio" />
                  </td> */}
                </tr>
              </tbody>
            </table>
          </div>
          {/* <div class="flex pl-4 mt-4 lg:w-2/3 w-full mx-auto">
            <a class="text-yellow-500 inline-flex items-center md:mb-2 lg:mb-0">
              Learn More
              <svg
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                class="w-4 h-4 ml-2"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14M12 5l7 7-7 7"></path>
              </svg>
            </a>
            <button class="flex ml-auto text-white bg-yellow-500 border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded">
              Button
            </button>
          </div> */}
        </div>
      </section>
    </div>
  );
}

export default TableRFM;