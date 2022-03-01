/**
 * @author Finn Kohlscheen
 */
const crypto = require("./crypto.js");
const Hashes = require("jshashes");
const SHA1 = new Hashes.SHA1();
import Localbase from "localbase";
let db = new Localbase("db");

const username = document.getElementById("inputEmail4");
const submitButton = document.getElementById("submitBTN");
const guestButton = document.getElementById("guestBTN");

submitButton.addEventListener("click", async () => {
  let acc_boolean = await db.collection("globalVars").doc({ id: 2 }).get()
  let key_boolean = await db.collection("globalVars").doc({ id: 1 }).get()
  
  // check DB if an account already exists
  if (acc_boolean.accountCreated)
    alert("You already have an account!");
  else if (username.value.length < 1) alert("Please enter a username!");
  else {
    if (!key_boolean.keysCreated) {
      // generate keypair
      await crypto.makeAndSaveKeys();
      await db.collection("globalVars").doc({ id: 1 }).set({ id: 1, keysCreated: true });
    } else {
      console.log("Keys already created!");
    }

    // get public key
    let publicKey = await crypto.getPublicKey();
    let to_sign = publicKey + username.value;
    // sign public key + username
    let signature = await crypto.sign(to_sign);

    let parameter_POST = {
      createAccount: {
        publicKey: publicKey,
        fingerPrintPublicKey: SHA1.hex(publicKey),
        publisherName: username.value,
        firstLogin: new Date().toISOString(),
        signatureOnPublicKeyPublisherName: signature,
      },
    };

    let req_msg = {
      method: "POST",
      parameter: JSON.stringify(parameter_POST),
    };

    chrome.runtime.sendMessage(req_msg, async (response) => {
      if (response.createAccount.status == "OK") {
        // save username
        await db.collection("users").add({ id: 1, username: username.value });
        // update createAccount boolean
        await db.collection("globalVars").doc({ id: 2 }).set({ id: 2, accountCreated: true });
        await db.collection("globalVars").doc({ id: 4 }).set({ id: 4, guestAccount: false });
        location.href="./home.html";
        alert("Account created successfully!");
      }
      else alert(response.createAccount.message);
    });
  }
});

if (guestButton != null) {
  guestButton.addEventListener("click", () => {
    db.collection("globalVars").doc({ id: 4 }).set({ id: 4, guestAccount: true });
  });
}
