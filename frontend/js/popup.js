/**
 * @author mlr-f & Finn Kohlscheen
 */

import Localbase from "localbase";
let db = new Localbase("db");

db.collection("globalVars").doc({ id: 2 }).get().then( async (acc_boolean) => {
  let guest_boolean = await db.collection("globalVars").doc({ id: 4 }).get();
  if (acc_boolean.accountCreated == false && guest_boolean.guestAccount == false) {
    location.href="./welcome.html";
  } else if (guest_boolean.guestAccount === true) {
    location.href="./homeGuest.html"
  }
}); 