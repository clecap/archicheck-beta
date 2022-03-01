# Archicheck Backend Tests
**Author**: Benjamin Müller
**Date**: December 2021

This document will protocol my testing approaches in regards of testing the archicheck backend. Currently the implementation of the database aswell as GET and POST requests are done. As stated in their current README.md file they are able to send JSON formatted strings with curl to the database and retrieve them with the help of POST messages again.

### Correct display and formatting
After talking with Paul from the backend team, we came to the conclusion that for the current point of time and developement its the best if tests start with checking if the string information over curl -d ... is converted correctly into the database and from there is returned correctly back to the user also regarding the specification of interface_description.md of the team narrative-description.

### Testing
For testing I created a total of ten requests by using POST and GET requests with the tool postman. I split them up into three collections. Collection one is responsible for the setup and clean up process.  Collection two is responsible for filling the database with test values, some wrong, some correct and collection three does further down explained checks regarding GET requests.

#### Setup/Cleanup
In the GET request INIT, I set up a certain amount of enviroment variables for Postman to work with. This is done to reduce redundancy. For example exchanging variables can now be done at one spot instead of having to change them everywhere in postman. That works because enviroment variables are accessible through multiple tests and collections.
```
pm.environment.set("urlToCheck", "faceBookLinkHash1234");
pm.environment.set("fingerPrintPublicKey", "123457854785");
pm.environment.set("publisherName", "Friedrich-factchecker");
pm.environment.set("URLwithFactCheck", "correctiveLink-1-Friedrich");
pm.environment.set("timestamp", "2021-03-15-12:24:11");
pm.environment.set("urlsignature-on-UrlToCheckHash-fingerPrint-URLwithfactCheck-timestamp", "568451235");
```
The cleanup process just includes clearing the current database. For this the backend team created an own endpoint which I am just calling with a POST request clearing the entire database. In that request aswell as the setup process nothing really is tested.

#### Post testing
Now we come to the part where we fill the database with test samples. Here we do a total of five POST requests. Currently three of these are false entries, one is a correct entry and one is a duplicate. It is important that after test one, two and three the database is cleaned with `localhost:8080/postendpoint/deleteDB`. This is done to ensure no unexpected behaviours occur.

Test one tries to send the following POST `localhost:8080/postendpoint` with the BODY of
```
{
    "publishNewFactCheck":{
        "test2":"hund"
    }
}
```
and checks if this returns a 400 ERROR code. Test two tries to use the right amount of values and attributes but has a spelling mistake in one of its attribute URLwithFactCheck whhich simply just has an additional 1 at its end: URLwithFactCheck**1**. This test expects a return value of 400.
```
{
    "publishNewFactCheck":{
        "urlToCheckHash":"faceBookLinkHash1234", 
        "fingerPrintPublicKey":"12457854785",
        "publisherName":"Friedrich-factchecker", 
        "URLwithFactCheck1":"correctivLink-1-Friedrich", 
        "timestamp":"2021-03-15-12:24:11", 
        "signature-on-UrlToCheckHash-fingerPrint-URLwithfactCheck-timestamp":"568451235"
    }
}
```
Test three has now an error in a type specific attribute field. For this I chose the attribute field of timestamp, which should be a timestamp. Here I entered the value that is not a timestamp. This test expects a return value of 400.
```
{
    "publishNewFactCheck":{
        "urlToCheckHash":"faceBookLinkHash1234", 
        "fingerPrintPublicKey":"12457854785",
        "publisherName":"Friedrich-factchecker", 
        "URLwithFactCheck":"correctivLink-1-Friedrich", 
        "timestamp":"abcd", 
        "signature-on-UrlToCheckHash-fingerPrint-URLwithfactCheck-timestamp":"568451235"
    }
}
```
Test four includes the first correct BODY content. Our example here is
```
{
    "publishNewFactCheck":{
        "urlToCheckHash":"faceBookLinkHash1234", 
        "fingerPrintPublicKey":"12457854785",
        "publisherName":"Friedrich-factchecker", 
        "URLwithFactCheck":"correctivLink-1-Friedrich", 
        "timestamp":"2021-03-15-12:24:11", 
        "signature-on-UrlToCheckHash-fingerPrint-URLwithfactCheck-timestamp":"568451235"
    }
}
```
The expected return value here is 200 OK. This test four is also used for test five, which inserts an identical JSON argument. The test expects the return to be 400.

#### Get testing
The get testing so far consists out of only three requests. This will later be expanded when new functionality is added by the backend team.
In test one simply tests if a request to the URL `localhost:8080/factChecks/*` is successful, meaning it returns the status 200 OK. Test two tests if the response time is below 200ms. This is to ensure that the application executes in a reasonable timeframe. The third test now checks through assertion if the entered values are processed correctly and returned correctly. Test two and three are also done with GET and the said URL.
**Example**:
```
let urlToCheckHash = pm.environment.get("urlToCheck");
pm.test("Saved Correctly", function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData.DB.urlToCheckHash).to.eql(urlToCheckHash);
}
```
### Further testing
The ideas and collections of tests are far from being complete. However at the current state of developement these tests make sure that the base of the application is running correctly. I will also continue expanding this document as soon as new things such as tests or collections are added to postman.