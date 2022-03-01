/**
 * @author Finn Kohlscheen
 */

const crypto = require("./crypto.js");
const Hashes = require("jshashes");
const SHA1 = new Hashes.SHA1();
const SHA512 = new Hashes.SHA512();
import Localbase from "localbase";
let db = new Localbase("db");

const yesButton = document.getElementById("yesButton");

yesButton.addEventListener("click", async () => {
    // delete FactChecks -> send delete account request to server

    // delete FactChecks
    let publicKey = await crypto.getPublicKey();
    let user = await db.collection("users").doc({ id: 1 }).get();
    db.collection("factChecks").get().then(async (result) => {
        // send delete request for every FactCheck
        for (let i=0; i < result.length; i++) {
            let urlToCheckHash = SHA512.hex(result[i].url);
            let to_sign = publicKey + user.username + urlToCheckHash + "DELETEFLAG";
            let signature = await crypto.sign(to_sign);

            let parameter_POST = {
                deleteFactCheck: {
                    publicKey: publicKey,
                    fingerPrintPublicKey: SHA1.hex(publicKey),
                    URLToCheckHash: urlToCheckHash,
                    URLwithFactCheck: result[i].factCheck,
                    signatureOnPublicKeyPublisherNameURLToCheckHashDELETEFLAG: signature,
                },
            };
            let req_msg = {
                method: "POST",
                parameter: JSON.stringify(parameter_POST),
            };
            chrome.runtime.sendMessage(req_msg, async () => {
                // delete IndexedDB entry of correspondent factCheck
                await db.collection('factChecks').doc({factCheck: result[i].factCheck}).delete();
            });
        }

        // send delete account request to server
        let fingerprint = SHA1.hex(publicKey);
        let to_sign2 = fingerprint + user.username + "DELETEFLAG";
        let signature2 = await crypto.sign(to_sign2);

        let parameter_POST2 = {
            deleteAccount: {
                publicKey: publicKey,
                fingerPrintPublicKey: fingerprint,
                publisherName: user.username,
                signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG: signature2,
            },
        };

        let req_msg2 = {
            method: "POST",
            parameter: JSON.stringify(parameter_POST2),
        };

        chrome.runtime.sendMessage(req_msg2, async (response) => {
            if (response.error != undefined) alert(response.error);
            else if (response.deleteAccount.status == "OK") {
                // update globalVars
                await db.collection("globalVars").doc({ id: 1 }).set({ id: 1, keysCreated: false});
                await db.collection("globalVars").doc({ id: 2 }).set({ id: 2, accountCreated: false});
                await db.collection("globalVars").doc({ id: 4 }).set({ id: 4, guestAccount: true});
                
                // delete key pair
                await db.collection("keys").doc({ id: 1 }).delete();

                // delete username
                await db.collection("users").doc({ id: 1 }).delete();

                location.href="./home.html";
                alert("Account deleted successfully!");
            } else alert("Something went wrong");
        });
    });
});
