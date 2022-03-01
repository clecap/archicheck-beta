/**
 * @author mlr-f & Finn Kohlscheen
 */
import Localbase from "localbase";
const crypto = require("./crypto.js");
let db = new Localbase("db");

chrome.runtime.onInstalled.addListener(async () => {
  // set global vars
  let redundancy_check = await db.collection("globalVars").get();
  console.log(redundancy_check)
  if (redundancy_check.length == 0) {
    await db.collection("globalVars").add({
      id: 1,
      keysCreated: false,
    });
    await db.collection("globalVars").add({
      id: 2,
      accountCreated: false,
    });
  
    await db.collection("globalVars").add({
      id: 3,
      allFactCheckers: true,
    });
    await db.collection("globalVars").add({
      id: 4,
      guestAccount: false,
    });
  }
});

console.log("background.js loaded...");

/*** START: configuration of the api ***/
const host = "http://localhost:8080/";
const endpoint_POST = "postendpoint";
/*** END: configuration of the api   ***/

/**
 * listening for 'GET' and 'POST' requests from the extension
 * and send the correct request to the static webserver
 */
chrome.runtime.onMessage.addListener((req_msg, sender, response) => {
  console.log(
    `[background.js] has been called for method: '${req_msg.method}'`
  );

  if (req_msg.method === "GET") {
    _low_level_call(req_msg, {}, response);
  } else if (req_msg.method === "POST") {
    let payload = {
      method: req_msg.method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: req_msg.parameter,
    };

    console.log(`Payload for POST Request:\n${payload.body}`);

    _low_level_call(req_msg, payload, response);
  }

  return true;
});

const _low_level_call = async (req_msg, payload, response) => {
  let finalHost =
    req_msg.method == "POST" ? host + endpoint_POST : host + req_msg.parameter;

  console.log(`[_low_level_call]: Calling '${finalHost}'`);

  await fetch(finalHost, payload)
    .then((res) => {
      console.log(`[1]: We got a result from the webserver.\n`);
      
      if (res.status === 400) {
        let error_msg = {
        error: `status code is '${res.status}', but should be '200'. statusText: ${res.statusText}`,
        text_msg:
          "[ERROR]: Bad response from the server.",
        };
        console.log(
        `[1]: An error occured during the procedure - ${error_msg.error}}`
      );
        response(error_msg);
        return;
      } else if (res.status === 404) {
        let error_msg = {
        error: `status code is '${res.status}', statusText: ${res.statusText}`,
        text_msg:
          "No data for given URL :-(",
        };
        console.log(
        `[1]: No data for given URL - ${error_msg.error}`
      );
        response(error_msg);
        return;
      }

      // convert response to json
      res
        .json()
        .then((json_rsp) => {
          console.log(`[2]: Valid json response.`);
          console.log("@@@@@@@@@@@@@@@");
          console.log(json_rsp);
          response(json_rsp)
        })
        .catch((err) => {
          console.log(`[2]: Invalid json response. \n[3]: ${err}`);
          let error_msg = {
            error: err,
            text_msg: "[ERROR]: Data is not in JSON. :-(",
          };
          response(error_msg);
          return;
        });
      return;
    })
    .catch((err) => {
      console.log(
        `[1]: An error occured during the procedure. - ${err}`
      );

      let error_msg = {
        error: `An error occured during the procedure: ${err}`,
        text_msg:
          "[ERROR]: The webserver is currently not available. Please try again later :-(",
      };
      response(error_msg);
      return;
    });

  return;
};

