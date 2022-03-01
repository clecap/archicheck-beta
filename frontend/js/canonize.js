/**
 * @author Josefine Riech
 * @author Norbert Scheffler
 */

console.log("canonize is loaded...");


//The body of this function will be injected into the target website if canonize() is called
function getCanonical(){
    //Request canonical tag value
    return document.querySelector("link[rel='canonical']").getAttribute("href");
}

//Check for Slash at the end and append, if necessary
function checkSlash(url){
    //Check, whether there already is a "/" at the end
    if (url.slice(-1) === "/") return url;
    //Otherwise, append one
    else {
        url = url + "/"
        return url;
    }
}

//Main canonize function, which is called from other parts of the extension
export function canonize(tab, callback){
    // Inject getCanonical() into the website of tab
    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        function: getCanonical
        },(results) => {
        //Fetch canonized URL form response of injected script
        let canonizedURL = results[0].result;
        //Now, do whatever is defined via callback
        //If there is no canonical Tag, we take the URL of the given tab as canonical (it has to end with "/")
        if (canonizedURL === null || canonizedURL === undefined) callback(checkSlash(tab.url));
        //If there is a canonical tag, we can just call the callback with a "slashed" URL
        else{
            if (canonizedURL.includes("twitter")){
                callback(checkSlash(tab.url));
            }
            else callback(checkSlash(canonizedURL));
        }
    });
}



