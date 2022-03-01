/**
 * @author Finn Kohlscheen
 */

import Localbase from "localbase";
let db = new Localbase("db");

const unsubscribeBtn = document.getElementById("unsubButton");
const selectList = document.getElementById("selectList");

db.collection("subscribed").get().then((result) => {
    if(result.length == 0) {
        let no_subscribed = document.createElement("option");
        no_subscribed.text = "You have not subscribed to a publisher yet";
        selectList.appendChild(no_subscribed);
    }
    else {
        for(let i=0; i < result.length; i++) {
            let publisher = document.createElement("option");
            publisher.text = result[i].publisherName;
            selectList.appendChild(publisher);
        }
    }
});

unsubscribeBtn.addEventListener("click", async () => {
    let publishers = await db.collection("subscribed").get();
    let selected = selectList.selectedIndex;
    await db.collection("subscribed").doc({ fingerPrintPublicKey: publishers[selected].fingerPrintPublicKey}).delete();
    location.reload();
});
