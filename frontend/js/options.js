/**
 * @author Finn Kohlscheen
 */

import Localbase from "localbase";
let db = new Localbase("db");

const saveButton = document.getElementById('saveOpt')

var selectedOpt;
let initial_setting;

// OPTIONS -- show subscribed or all FactChecks
db.collection('globalVars').doc({ id: 3 }).get().then(result => {
    initial_setting = result.allFactCheckers;

    if (result.allFactCheckers == true){
        document.getElementById("allFC").checked = true;
    }
    if (result.allFactCheckers == false){
        document.getElementById("myFC").checked = true;
    }
  });

saveButton.addEventListener("click", () => {
    selectedOpt = document.querySelector('input[name="chosenFCs"]:checked').value;
    
    /* store selected Option in IndexedDB */
    if (selectedOpt == "allFC" && initial_setting == false){
        db.collection("globalVars").doc({ id: 3 }).set({id: 3, allFactCheckers: true})
        alert("Setting changed");
    }
    if (selectedOpt == "myFC" && initial_setting == true) {
        db.collection("globalVars").doc({ id: 3 }).set({id: 3, allFactCheckers: false})
        alert("Setting changed");
    }
});
