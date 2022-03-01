/**
 * @author mlr-f
 */

const Hashes = require("jshashes");
const crypto = require("./crypto.js");
const SHA512 = new Hashes.SHA512();
const SHA1 = new Hashes.SHA1();
const { canonize } = require("./canonize");
const { is_url } = require("./crypto")
import Localbase from "localbase";
let db = new Localbase("db");

const submitButton = document.getElementById("submit");
const url_text = document.getElementById("url-input");

submitButton.addEventListener("click", () => {

  if (!is_url(url_text.value)) {
    alert("Your input is not a valid URL. Ignoring input.")
    return;
  }
  
  chrome.tabs.query(
    {
      active: true,
      currentWindow: true,
    },
    async (tabs) => {
      if (!is_url(tabs[0].url) || tabs[0] === undefined) {
        alert("Can't publish your Factcheck. Invalid URL for the website you want to publish.")
        return
      }
      canonize(tabs[0], (canonizedURL) => { 
        // we take the "normal" URL if we cant get the canonicalURL
        if (canonizedURL === undefined) {
          canonizedURL = tabs[0].url
        } 
        publishNewFactCheck(canonizedURL)
      })
    }
  );
});

const publishNewFactCheck = async (canonizedURL) => {
  const url_to_check_hash = SHA512.hex(canonizedURL)

  let fingerprint = SHA1.hex(await crypto.getPublicKey());
  // let publisher = await db.collection("users").doc({ id: 1 }).get()
  let curr_ts = new Date().toISOString();
  let factcheck_for_url = url_text.value;
  let to_sign =
    url_to_check_hash + fingerprint + factcheck_for_url + curr_ts;
  let signed = await crypto.sign(to_sign);
      
  let parameter_POST = {
    publishNewFactCheck: {
      URLToCheckHash: url_to_check_hash,
      fingerPrintPublicKey: fingerprint,
      //publisherName: publisher.username,
      URLwithFactCheck: factcheck_for_url,
      timestamp: curr_ts,
      // ! should be moved to 'signatureOnPublisherNameURLToCheckHashFingerPrintURLwithfactCheckTimestamp'
      signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp: signed,
    },
  };

  let req_msg = {
    method: "POST",
    parameter: JSON.stringify(parameter_POST),
  };

  chrome.runtime.sendMessage(req_msg, (response) => {
    if (response.error !== undefined) {
      console.log(response)
      alert("You already published that Factcheck for the website you're currently on! ")
    }
    else if (response.publishNewFactCheck.status === "OK") {
      alert("Published new FactCheck!");     
      // save URL + factCheck in IndexedDB
      db.collection("factChecks").add({
        url: canonizedURL,
        factCheck: factcheck_for_url
      });
    } 
  });
}