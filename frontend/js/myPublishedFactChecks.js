/**
 * @author Finn Kohlscheen
 */
// file for checking users own published factChecks

const crypto = require("./crypto.js");
const Hashes = require("jshashes");
const SHA1 = new Hashes.SHA1();
const SHA512 = new Hashes.SHA512();
import Localbase from "localbase";
let db = new Localbase("db");

const buttons = document.getElementsByClassName("btn");


// placeholder factChecks
//db.collection("factChecks").add({url: "notAUrl.com", factCheck: "lalala"});
//db.collection("factChecks").add({url: "correctiv.org", factCheck: "this is factCheck"});
//db.collection("factChecks").add({url: "yoyo.com", factCheck: "blabla"});

// get URLs and factChecks from IndexedDB
db.collection("factChecks")
  .get()
  .then((result) => {
    let list_grp = document.getElementsByClassName("list-group-item list-group-item-action");

    if (result[0] == undefined) {
      for (let i = 0; i < list_grp.length; i++) {
        if (i == 0)
          list_grp[i].innerHTML = "You have not published a FactCheck yet!";
        else list_grp[i].remove();
      }
    } else {
      // fill the list with URL and factChecks
      for (let i = 0; i < list_grp.length; i++) {
        if (result[i] == undefined) {
          list_grp[i].remove();
        }
        else {
          let a = document.createElement("a");
          a.setAttribute("href", result[i].url);
          a.innerHTML = `[${result[i].url}]:`;
          a.setAttribute("target", "_blank");
          list_grp[i].appendChild(a);

          let b = document.createElement("b");
          b.innerHTML =
            " <a target='_blank' href=" +
            result[i].factCheck +
            ">Your FactCheck</a>";
          list_grp[i].appendChild(b);
        }
      }
    }

    // EventListeners for all delete-buttons
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", async () => {
        console.log("clicked Button: ", i);

        // send "delete fact check"-request to server
        let publicKey = await crypto.getPublicKey();
        let user = await db.collection("users").doc({ id: 1 }).get();
        let urlToCheckHash = SHA512.hex(result[i-1].url);
        let to_sign = publicKey + user.username + urlToCheckHash + "DELETEFLAG";
        let signature = await crypto.sign(to_sign);

        let parameter_POST = {
          deleteFactCheck: {
            publicKey: publicKey,
            fingerPrintPublicKey: SHA1.hex(publicKey),
            URLToCheckHash: urlToCheckHash,
            URLwithFactCheck: result[i-1].factCheck,
            signatureOnPublicKeyPublisherNameURLToCheckHashDELETEFLAG: signature,
          },
        };
        let req_msg = {
          method: "POST",
          parameter: JSON.stringify(parameter_POST),
        };
        chrome.runtime.sendMessage(req_msg, async (response) => {
          if (response.error != undefined) alert(response.error);
          else if (response.deleteFactCheck.status == "OK") {
            // delete IndexedDB entry of correspondent factCheck
            await db.collection('factChecks').doc({factCheck: result[i-1].factCheck}).delete();
            location.reload();
            alert("FactCheck deleted");
          } else alert("Something went wrong");
        });
      });
    }
  });
