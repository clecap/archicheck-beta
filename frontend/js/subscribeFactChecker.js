/**
 * @author Finn Kohlscheen & mlr-f
 */

const crypto = require("./crypto.js");
import Localbase from "localbase";
let db = new Localbase("db");

const selectList = document.getElementById("selectList");
const subscribeBtn = document.getElementById("subscribeButton");
const searchField = document.getElementById("searchField");
const searchBtn = document.getElementById("searchButton");

// list of publishers from all pages sent by backend
let allPagesPublisher = [];

// compares fingerprint of publisher from backend and IndexedDB
const checkFingerPrint = (array, fingerPrint) => {
  for (let i = 0; i < array.length;  i++){
    if (array[i].fingerPrintPublicKey === fingerPrint) {
      return true;
    }
  }
  return false;
}

// TODO: for loop for every page
const req_msg = {
  method: "GET",
  parameter: "publishers/page/1",
};

chrome.runtime.sendMessage(req_msg, async (response) => {
  if (response.allPublishers.status != "OK") alert("An error occured during the request :(");
  else {
    let publisherList = response.allPublishers.publisherList;
    let alreadySubscribed = await db.collection("subscribed").get();
  
    for(let i=0; i < publisherList.length; i++) {    
      // verifiy the signatureOnPublicKeyPublisherName
      const publicKeyIMPORTED = await crypto.importPublicKey(publisherList[i].publicKey);
      const to_verify = publisherList[i].publicKey + publisherList[i].publisherName;
      const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, publisherList[i].signatureOnPublicKeyPublisherName);
      
      // dont display publisher if already subscribed or invalid signature
      if (checkFingerPrint(alreadySubscribed, publisherList[i].fingerPrintPublicKey) || !is_verified) continue;
      
      let publisher = document.createElement("option");
      publisher.text = publisherList[i].publisherName;
      selectList.appendChild(publisher);
      allPagesPublisher.push(publisherList[i]);
    }
  }
});

subscribeBtn.addEventListener("click", async () => {
  if (selectList.selectedIndex != -1) {
    let selected = selectList.selectedIndex;
    let new_publisher = allPagesPublisher[selected];
    await db.collection("subscribed").add(new_publisher);
    location.reload();
  }
});

// search by username or fingerprint
searchBtn.addEventListener("click", () => {
  if (searchField.value.length > 0) {
    let parameter_POST = {
      searchPublisher: {
        searchTerm: searchField.value,
        timestamp: new Date().toISOString(),
      },
    };

    let req_msg2 = {
      method: "POST",
      parameter: JSON.stringify(parameter_POST),
    };

    chrome.runtime.sendMessage(req_msg2, async (response) => {
      if (response.searchPublisher) alert(response.searchPublisher.message);
      else {
        let alreadySubscribed = await db.collection("subscribed").get();

        // search by PublisherName
        if (response.searchPublishersResult.hasResultByFingerPrint == false) {
          let publisherList = response.searchPublishersResult.resultsByPublisherName;

          // clear current list
          selectList.options.length = 0;

          // put publishers you searched for in list
          for(let i=0; i < publisherList.length; i++) {
            // verifiy the signatureOnPublicKeyPublisherName
            const publicKeyIMPORTED = await crypto.importPublicKey(publisherList[i].publicKey);
            const to_verify = publisherList[i].publicKey + publisherList[i].publisherName;
            const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, publisherList[i].signatureOnPublicKeyPublisherName);

            // dont display publisher if already subscribed or invalid signature
            if (checkFingerPrint(alreadySubscribed, publisherList[i].fingerPrintPublicKey) || !is_verified) continue;

            let publisher = document.createElement("option");
            publisher.text = publisherList[i].publisherName;
            selectList.appendChild(publisher);

          }
        }
        // search by PublicKeyFingerPrint
        else {
          let publisher_fp = response.searchPublishersResult.resultByFingerPrint;
          selectList.options.length = 0;

          const publicKeyIMPORTED = await crypto.importPublicKey(publisher_fp.publicKey);
          const to_verify = publisher_fp.publicKey + publisher_fp.publisherName;
          const is_verified = await crypto.verify(publicKeyIMPORTED, to_verify, publisher_fp.signatureOnPublicKeyPublisherName);

          if (!checkFingerPrint(alreadySubscribed, publisher_fp.fingerPrintPublicKey) && is_verified) {
            let publisher = document.createElement("option");
            publisher.text = publisher_fp.publisherName;
            selectList.appendChild(publisher);
          }
        }
      };
    });
  };
});
