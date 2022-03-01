/**
 * @author mlr-f
 */

const {is_url} = require("./crypto.js")
const Hashes = require("jshashes");
const SHA512 = new Hashes.SHA512();
const crypto = require("./crypto.js");
const {canonize} = require("./canonize");
import Localbase from "localbase";

let db = new Localbase("db");

// get the list where we want to show the factChecks
let list_grp = document.getElementById("factcheck-list");

chrome.tabs.query(
  {
    active: true,
    currentWindow: true,
  },
  async (tabs) => {
    if (!is_url(tabs[0].url) || tabs[0] === undefined) {
      let list_item = document.createElement("li")
      list_item.className = "list-group-item"
      let a = document.createElement("a")
      a.innerText = `Can't get an URL for the current website..`;
      list_item.append(a)
      list_grp.appendChild(list_item)
      return;
    }
    //Calling canonize with active tab and usage-callback
    canonize(tabs[0], (canonizedURL) => {
      console.log("Canonical URL: " + canonizedURL)

      if (canonizedURL === undefined) {
        canonizedURL = tabs[0].url
      }
      
      factChecksForWebsite(canonizedURL)
    });
  }
);

const factChecksForWebsite = async (canonizedURL) => {
  let allFactChecks = (await db.collection("globalVars").doc({ id: 3 }).get()).allFactCheckers
  let url_to_check_hash = SHA512.hex(canonizedURL)
  
  // get the list off all publisher who published for the requested URL
  let req_msg = {
    method: "GET",
    parameter: "publishers/" + url_to_check_hash + "/*",
  };
  
  chrome.runtime.sendMessage(req_msg, (response) => {
    if (response.error !== undefined) {
      let list_item = document.createElement("li")
      list_item.className = "list-group-item"
      let a = document.createElement("a")
      a.innerText = response.text_msg;
      list_item.append(a)
      list_grp.appendChild(list_item)
      return;
    }
    else {
      if (allFactChecks) {
        let { publishersForSpecificLink } = response
        let requested_publisher = []
      
        // request the factCheck for each publisher
        publishersForSpecificLink.forEach(async (publisher) => {
              
          // make sure to send the URL req only once per publisher
          if (requested_publisher.includes(publisher.fingerPrintPublicKey)) { return; }
          else { requested_publisher.push(publisher.fingerPrintPublicKey); }
              
          // verifiy the signatureOnPublicKeyPublisherName
          const publicKeyIMPORTED = await crypto.importPublicKey(publisher.publicKey)
          const to_verify = publisher.publicKey + publisher.publisherName
          const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, publisher.signatureOnPublicKeyPublisherName)
          console.log(`Valid signature for publisher: '${publisher.publisherName}'? --> ${is_verified}`)

          if (!is_verified) {
            return
          }

          let req_msg = {
            method: "GET",
            parameter: `factChecks/${url_to_check_hash}/${publisher.fingerPrintPublicKey}`
          };

          chrome.runtime.sendMessage(req_msg, async (response) => {
              
            if (response.error !== undefined) {
              // dont display error factchecks
              return;
            }
        
            let {specificFactCheck} = response
              
            specificFactCheck.forEach(async (factCheck) => {
              // ! 'signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp' will be changed to 'signatureOnPublisherNameURLToCheckHashFingerPrintURLwithfactCheckTimestamp'
              // verify the signature of each factCheck
              const to_verify = url_to_check_hash + publisher.fingerPrintPublicKey + factCheck.URLwithFactCheck + factCheck.timestamp
              const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, factCheck.signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp)
              console.log(`Valid signature for publisher: '${publisher.publisherName}' with factCheck: ${factCheck.URLwithFactCheck}? --> ${is_verified}`)
              if (!is_verified) {
                return
              }
              giveFactCheckToHTML(factCheck.URLwithFactCheck, publisher.publisherName)  
            })
          })
        })
      } else {
        // get the list off all subscribed publisher from the user. Send the req only for that list
        db.collection("subscribed").get().then(async (result) => {
          if (result.length === 0) {
            let list_item = document.createElement("li")
            list_item.className = "list-group-item"
            let a = document.createElement("a")
            a.innerText = "No subscribed publishers. Nothing to see."
            list_item.append(a)
            list_grp.appendChild(list_item)
            return
          }
          let noFactChecks = true

          result.forEach((subscribedPublisher) => {
            let req_msg = {
              method: "GET",
              parameter: `factChecks/${url_to_check_hash}/${subscribedPublisher.fingerPrintPublicKey}`
            };
          
            chrome.runtime.sendMessage(req_msg, async (response) => {
              if (response.error !== undefined) {
                // dont display error factchecks
                return;
              }

              let { specificFactCheck } = response

              const publicKeyIMPORTED = await crypto.importPublicKey(subscribedPublisher.publicKey)

              specificFactCheck.forEach(async (factCheck) => {
                // verify the signature of each factCheck
                const to_verify = url_to_check_hash + subscribedPublisher.fingerPrintPublicKey + factCheck.URLwithFactCheck + factCheck.timestamp
                const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, factCheck.signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp)
                console.log(`Valid signature for publisher: '${subscribedPublisher.publisherName}' with factCheck: ${factCheck.URLwithFactCheck}? --> ${is_verified}`)
                if (!is_verified) {
                  return
                }
                giveFactCheckToHTML(factCheck.URLwithFactCheck, subscribedPublisher.publisherName)
                noFactChecks = false
              })
            })
          });
          setTimeout(() => {
            if (noFactChecks === true) {
              let list_item = document.createElement("li")
              list_item.className = "list-group-item"
              let a = document.createElement("a")
              a.innerText = "No factchecks by your subscribed publishers for this URL"
              list_item.append(a)
              list_grp.appendChild(list_item)
            }
          }, 250)
        });
      }
    }
  });
}

const giveFactCheckToHTML = (urlWithFactCheck, publisherName) => {
  let list_item = document.createElement("li")
  list_item.className = "list-group-item"
  let a = document.createElement("a")
  a.setAttribute("href", urlWithFactCheck);
  a.innerText = `FactCheck by: ${publisherName}`;
  a.setAttribute("title", urlWithFactCheck);
  a.setAttribute("target", "_blank");
  list_item.append(a)
  list_grp.appendChild(list_item)
  return;
}