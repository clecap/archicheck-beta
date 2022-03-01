# Archicheck Backend Tests
**Author**: Benjamin Müller  
**Date**: 13.01.2022 - 31.01.2022

This document will protocol my testing approaches in regard to testing the archicheck backend. Currently, the 
implementation of the database as well as GET and POST requests are done. More specifically it is now possible to add
new users to the database as well as new fact checks. There is also a Hash and Crypto functionality implemented that does
internally checks if user and fact checker entries are done validly. As stated in their current README.md file 
they are able to send JSON formatted strings with curl to the database and retrieve them with the help of POST messages 
again.

# Adapting current postman testing setup
Currently, there are many things that have changed which break the already implemented functionality regarding the 
Postman application. One of these things is that one attribute field "publisherName":"<publisher-name>" got removed. 
Therefore, I adapted the generic adding of the fact check accordingly:
```json
{
    "publishNewFactCheck":{
        "URLToCheckHash":<hash>,
        "fingerPrintPublicKey":<fingerprint>,
        "URLwithFactCheck":<URL>,
        "timestamp":<timestamp,
        "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":<signature>
    }
}
```

Furthermore, I added users to the postman collection system. This can be simply done by creating
a new POST request, selecting the *body* tab and choosing the field *raw*. There you can enter the body in JSON format:
```json
{
    "createAccount":{
        "publicKey":<publickey>,
        "fingerPrintPublicKey":<fingerprint>,
        "publisherName":<name>,
        "firstLogin":<timestamp>,
        "signatureOnPublicKeyPublisherName":<signature>
    }
}
```

# Usage of collections in Postman
Collections are useful to structure certain tests and/or prepare the environment so that it can be tested in.
In this section I will explain what collections I think are useful for testing and which are currently already 
implemented.

Generally, a simple test contains out of four parts. Firstly it checks if the request is OK or ERROR. Then it checks if
request contains a BODY and after that it checks if the request contains JSON. This is important because otherwise
Postman would run into problems. Also, it makes it more obvious where errors occur if they occur. For example:
```javascript
pm.test("Request ERROR", function () {
    pm.response.to.be.error;
});

pm.test("Request WITH BODY", function () {
    pm.response.to.be.withBody;
});

pm.test("Request WITH JSON", function () {
    pm.response.to.be.json;
});

pm.test("JSON is not wellformed.", function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData.publishNewFactCheck.message).equals("JSON is not wellformed.")
});
```

# Structure of the unit tests
Every unit test is structured in collections and folders. We divide into two main collection categories. "Correct" 
requests go into the collections that start with "Correct". Purposefully incorrect requests go into the collections that
start with "Incorrect". Furthermore, these collections are divided into sub categories. "ADD", "CHANGE" and "REVOKE"
which are the current main usages for POST requests. Furthermore, there is a second category for the GET requests. Here
we have the four main categories "FACTCHECK" which represents the use case #1 from interface-description.md, 
"PUBLISHER_FACT" which represents the use case #2, "PUBLISHER" which represents use case #3 and "REVOKE" which represents
use case #4.


## POST Requests
### Correct ADD
This collection holds all the tests that came to my mind when trying to fill the database. It has to be taken care
that this collection only contains POST requests that are correct and will be accepted by the server. Currently, there are four different user and 
five different fact checks that are inserted into the database. Also, important to mention that in the collection, all 
requests are checked to have the response to be OK.

Example User:
```json
{
    "createAccount":{
        "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqrp9b+gh7PQXOAQVnHbnPswXAX6/dZ3UYkU+KQ7TTPzp+pRudifRvqn7/cqx4zbAfDwf1beZEtjxK6KR16zxqPAQ5m0hEeboVDQk7zTUU8BlFEs3TfhwubK/OJSROyRGhpH+Cx9oMIJNDA9p3Pn74RrgkKwqEpkXUOAx/ld6U39gVxC2uhUMwtmHG1h305tWc4THVpz/nElazuqKtpC7H8mAJmfQcHV5uGm1JoLivKiCQR1l6L8JVjB5x9rINepfljAWvLMZxIqjhEppC3TW6+Gv3/6dxvwSvPrfN525MQOYEW2Cz8nq6r4lTqs5XX8dVXZ3Dqa+P8Vdg3zpU6pUfo8zavHOeGkJHiexS37fdMWGC1A/XkqTCEat5ycM5o/Kms1ox/Nza/tVi+Z2/+cZgGa9YIplaqxrWdJjCwAwJ0xAsCqz3hPTgCmP2LXwRzTrBhvrky6+d48Xcbeqst6Ut9RCNe+Aj/6nDnNBQvNt7oFvVM6Lhw6Ux9d462Mt3uF75doXIJbwczjW3IAYDHnBHbVd9V+feZNDm0IRWo3p9yINu/fIQEQKaMsSHxtxm8oTdwi/BVULhyaSXS3+gcRDMjdrB+u71ictb+iffdSX86e6d/60ouX6M1t/mdh7qFDNdMV9n7eE59Gy0jp/u9NekMkbVnvTUH9bcRAuF4o30zMCAwEAAQ==",
        "fingerPrintPublicKey":"1d3f4630d911fea226898a7a3116166b3a96b06f",
        "publisherName":"power-factchecker",
        "firstLogin":"Mon, 15 Nov 2021 14:06:44 GMT",
        "signatureOnPublicKeyPublisherName":"08f5e87f9ee6db7c6767791c9006537e3d358c578acc7d790f2b83450bd00f55c4727e49d66fee0de7de4afc262553ce65064846a7dcba37648d0c68442b773ece10be2afa37f53c171f469305b01acdd6d448fd8aec48ec6346651dfe2ed9b62815b0cd976e9331979019df1c3ef2af36177f8cb145be3fd56438e90fc309e1b16418eef317bbfdf67072427a8d3d564d8c0e050e445de25588ab3f1f3aa32fdd64c122892ba2dca2e5fccc836048c37bae3d2528be41a8fbb013e4a9f1a8bedbc8121878658ddfe8fe168e6f9661401cdb2f503356c1c340616573b5fe711b346f6d3ce2438bd3d976df1887e2b753ad82b1f6073961a1c4634e5836757e0e3b37385d2f304949e287354cf6c61a07382b9e3277341561d29d0e50764c55130d48e378b34b43932e20e4cbf3cc8738d612d00064dfda3f0dd1d0600292c436f8b4d92f28687b61d806e75da399aea9b19daff9763e2c6a078dc1e7fc31f4d8cbe0fe53d36cb75f92abca898ba410775592639a2bdd8b3512874432578e3205fb5e6f797206d9b85a6433d969363a932a87a856433f47d5e92f695ecee1c4566db9c5f6b928cb60655a7fd7b339941eec86205c69c69794066fe11919ae9e7c33d08f8de24c60dd2ed09e244a89799cd593035934684df5dab3f53cbb497fcbecef22cf8997ba027d0fd3475c3f47386bec06bad097ca2d11a8726ceeb17b69"
    }
}
```
Example FactCheck:
```json
{
  "publishNewFactCheck":{
    "URLToCheckHash":"f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93",
    "fingerPrintPublicKey":"1d3f4630d911fea226898a7a3116166b3a96b06f",
    "URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/01/angebliches-tucholsky-gedicht-ueber-impfungen-stammt-von-satire-autor/",
    "timestamp":"Sat, 18 Dec 2021 13:10:44 GMT",
    "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"3ae94ad9210e7700eb9a300c6af8f76a85a68371cb91b2bbf88f91962c8647d122f6754feb25bd60a91f7321ff585277726de01a9aee2b95b8d5c4fe44219e0ed07e615fc9908bbd80572f46702ce6e618cbf187847fb3cce69976472403caca52e0914953065afe4a696484a1931080b33229d82015664f1b12106750c863e6a7318285222c6528adb5eeabd83fb31cb1606bf8cfb83eb45a57558ae807f7368bc067e6d1cbd0b6d0bec5165b88e515838c5458cab6eb3f432e1da618cb2d4e0ec75edb2ae0840e15b550c456d7f174ceb4cc10d490eebbdf9560b8fde5573ca342d5080246d353098290d51c67833dad76cd451a7b6ec5b3c7d6986e8ba8bdb0b1130dceb1b01551eac2ac7b6862d56eab7899da5eec155db757fa920ea2e24bd9ebcd63cda33f4f0ea716ba05fdbda3f5d972b62f2d2754242f11cc0aeaa337fda7c0cba03b096c8c7d9ee60420efe86f4c37ce1e28a1d099863f8676ed96fe6b7a4534e26d7fee0ca3c96df55f07fabc021ac6be0476cf0c67fcbecf2014999bdb34107fa0045e906e8b0a5554b218ca9348d26940ec83b25409d68f0934925b255c436ed4d5098213a72f8da533e0d830bb6f3cadb6012a69a56197711f68f1f11e65fe0f2fabcb7ad43eb18e22ea9e0b0f4885b4cd4bc7f1b246d8042577fddf4ae2db0afa1542bbd3e743d2f6c49c97e545b61a89e6fc51d254e1d3f9"
  }
}
```

### Correct CHANGE
Holds one a test for changing the publisher name.  
**PROBLEM**: Doesn't work on main + need test data for testing it. (Tested on main - 24.01). Am not able to make issue-49
run on my PC.

Example:
```json
{
    "changePublisherName":{
        "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr1faDzSg07x+5hvEDGzUzpSkedtQaq0CHJV8MZrRXXUVOQ21a0eBnoVMZLADuBISyW0gj6nJ9dtu+T+KFUxJKuDIIVfNPMqmehPqqWxv8qRsUQywaRBnWm4QIW2I8BdQINvvDULFO6nG3DknyzYku3HPA+TVt147opqWqTUPivkBuEJN/ANroAq1P9WlrjbyFSdqHtuPDavXaVwq8JZhxKqhE4w0aAGryE5HCDIT1hAq42G2CC5NNW3IaZVBBMqPn/tNCp0sQtUJiQZ19erolrcAxVIFd4Rv+YuMSpYKXuyFHPcUUjwLGyj7wq5mE9YRp+xnQ0RHLl3JSoyJeGAQCKD1M6d2mI1sBP/kqQS9xFWmvDbHG9XnGrYRAWFPlEln8gPF4WyhSqDyX7959gfhowGZJksZk9l9Ofbr9BWpOp65Aib4TQJXRgfeMkmDsYneF7e2p+4Watbbe7KBlvMgR6YIRq9OYbSGPAikdVet/j0A9SAKY0DZhq2FRlzG2RAiIV0GvI+j5aZs3d4ljjy6VVK/O3URKL4znOM6mRZUl0Fq7Jo5c0JDFgeXorGbqo8RHKeSmMHh8O37sj1V1p6AWgtJgu4cSkFPkxqUp7z9XHZo/KZaUAf8YfzTqQGThTS6MpqVczrKXYsdghwFAtBep+Ba+QKuYVVIpPbwgGRyCmsCAwEAAQ==",
        "fingerPrintPublicKey":"075966285278f8dbc92b49342ede3869b1a75cec",
        "publisherName":"real-factchecker",
        "newPublisherName": "checkey-factfredder",
        "timestamp":"Mon, 22 Nov 2021 14:06:44 GMT",
        "signatureOnFingerPrintPublicKeyPublisherNameNewPublisherNameTimestampCHANGEFLAG":"8e20534defb6844f12b5942f73dde15ebd5e1ddeb77ddddda57fbc700cc984112d74c516560eb21374c4eabdcd717190f5a128309f668c9ba070d6dbe7f8ffea6251f1ee9877783ad61565354a095acf83382654c4078ab70ccc88b8f75eefc7f98dd38505cb7b30d49852d0b313faf483aef9af2a5a492dd6cfa52c0e59518f2f2cccdf82193433c56b545a79b6dc5f452eec4b2de01cb0168306ea4e0431277940fb4e977caf458295afe01e34a65934066aebc984c599ff2a6fa4dadd72b846f27199ada09b5aef74a13cbdb48c0fd9a1427f5bba747939ab06e64b9d4f090a67e7a3966ce28ea68b2177005c7d379079ab326347970c121804997c25337eb4677850f7684662ab3b588cb48c250e7c9649f7407380bb5e82d43438dba51cc7755dd894f6d2c9b7a3c73133522505903e7efb4b9b437bd9da6388ef66ef4c81e3096b0c0beca1f4b15bfc8c3237e12f00a7b58647d935cbe2b9c2b32923d4c36d8e18489ada5ead380858009424559949b1943cbd18fa192422d44699622629ccab2ebb935831a8dc7b837ce5106854e4f7b9cecdb325a09a26b03eed5dc4b6f0d071df2610137cc13ef678f926fa370f6821f02c251c41c7bcbccf23e25cf2800497c2768f89963fa84ee8a85d30d1ffc3173d926b732937bc78c55ef6f14c60e1e8a7c0776a5750afed436122829309c23034c5fcdf12bba589f6ea1c32"
    }
}
```

### Correct DELETE 
Holds one a test for changing the publisher name.  
**PROBLEM**: Doesn't work on main + need test data for testing it. (Tested on main - 24.01). Am not able to make issue-49
run on my PC.

Example:
```json
{
    "deleteAccount":{
        "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr1faDzSg07x+5hvEDGzUzpSkedtQaq0CHJV8MZrRXXUVOQ21a0eBnoVMZLADuBISyW0gj6nJ9dtu+T+KFUxJKuDIIVfNPMqmehPqqWxv8qRsUQywaRBnWm4QIW2I8BdQINvvDULFO6nG3DknyzYku3HPA+TVt147opqWqTUPivkBuEJN/ANroAq1P9WlrjbyFSdqHtuPDavXaVwq8JZhxKqhE4w0aAGryE5HCDIT1hAq42G2CC5NNW3IaZVBBMqPn/tNCp0sQtUJiQZ19erolrcAxVIFd4Rv+YuMSpYKXuyFHPcUUjwLGyj7wq5mE9YRp+xnQ0RHLl3JSoyJeGAQCKD1M6d2mI1sBP/kqQS9xFWmvDbHG9XnGrYRAWFPlEln8gPF4WyhSqDyX7959gfhowGZJksZk9l9Ofbr9BWpOp65Aib4TQJXRgfeMkmDsYneF7e2p+4Watbbe7KBlvMgR6YIRq9OYbSGPAikdVet/j0A9SAKY0DZhq2FRlzG2RAiIV0GvI+j5aZs3d4ljjy6VVK/O3URKL4znOM6mRZUl0Fq7Jo5c0JDFgeXorGbqo8RHKeSmMHh8O37sj1V1p6AWgtJgu4cSkFPkxqUp7z9XHZo/KZaUAf8YfzTqQGThTS6MpqVczrKXYsdghwFAtBep+Ba+QKuYVVIpPbwgGRyCmsCAwEAAQ==",
        "fingerPrintPublicKey":"075966285278f8dbc92b49342ede3869b1a75cec",
        "publisherName":"real-factchecker",
        "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG":"8e20534defb6844f12b5942f73dde15ebd5e1ddeb77ddddda57fbc700cc984112d74c516560eb21374c4eabdcd717190f5a128309f668c9ba070d6dbe7f8ffea6251f1ee9877783ad61565354a095acf83382654c4078ab70ccc88b8f75eefc7f98dd38505cb7b30d49852d0b313faf483aef9af2a5a492dd6cfa52c0e59518f2f2cccdf82193433c56b545a79b6dc5f452eec4b2de01cb0168306ea4e0431277940fb4e977caf458295afe01e34a65934066aebc984c599ff2a6fa4dadd72b846f27199ada09b5aef74a13cbdb48c0fd9a1427f5bba747939ab06e64b9d4f090a67e7a3966ce28ea68b2177005c7d379079ab326347970c121804997c25337eb4677850f7684662ab3b588cb48c250e7c9649f7407380bb5e82d43438dba51cc7755dd894f6d2c9b7a3c73133522505903e7efb4b9b437bd9da6388ef66ef4c81e3096b0c0beca1f4b15bfc8c3237e12f00a7b58647d935cbe2b9c2b32923d4c36d8e18489ada5ead380858009424559949b1943cbd18fa192422d44699622629ccab2ebb935831a8dc7b837ce5106854e4f7b9cecdb325a09a26b03eed5dc4b6f0d071df2610137cc13ef678f926fa370f6821f02c251c41c7bcbccf23e25cf2800497c2768f89963fa84ee8a85d30d1ffc3173d926b732937bc78c55ef6f14c60e1e8a7c0776a5750afed436122829309c23034c5fcdf12bba589f6ea1c32"
    }
}
```

### Incorrect ADD
This collection divides itself further down into:
- duplicates
- JSON format errors
- no/random use case defined
- wrong values

It is good to notice that the tests have further information in their folder structure and name. This makes it really
easy to figure out what exactly went wrong. For example:
![img.png](picture/img.png)
From this small example we can immediately see that the requests writes a user into the database. If we now look at the
structure of the folder, we see that there is a wrong value used, for a user, on its fingerprint and that a symbol
was removed there.

Example User (Missing all attributes):
```json
{"publishNewFactCheck":{}}
```
Example FactCheck (Missing attribute):
```json
{
    "publishNewFactCheck":{
        "URLToCheckHash":"f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93",
        "fingerPrintPublicKey":"1d3f4630d911fea226898a7a3116166b3a96b06f",
        "timestamp":"Sat, 18 Dec 2021 13:10:44 GMT",
        "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"3ae94ad9210e7700eb9a300c6af8f76a85a68371cb91b2bbf88f91962c8647d122f6754feb25bd60a91f7321ff585277726de01a9aee2b95b8d5c4fe44219e0ed07e615fc9908bbd80572f46702ce6e618cbf187847fb3cce69976472403caca52e0914953065afe4a696484a1931080b33229d82015664f1b12106750c863e6a7318285222c6528adb5eeabd83fb31cb1606bf8cfb83eb45a57558ae807f7368bc067e6d1cbd0b6d0bec5165b88e515838c5458cab6eb3f432e1da618cb2d4e0ec75edb2ae0840e15b550c456d7f174ceb4cc10d490eebbdf9560b8fde5573ca342d5080246d353098290d51c67833dad76cd451a7b6ec5b3c7d6986e8ba8bdb0b1130dceb1b01551eac2ac7b6862d56eab7899da5eec155db757fa920ea2e24bd9ebcd63cda33f4f0ea716ba05fdbda3f5d972b62f2d2754242f11cc0aeaa337fda7c0cba03b096c8c7d9ee60420efe86f4c37ce1e28a1d099863f8676ed96fe6b7a4534e26d7fee0ca3c96df55f07fabc021ac6be0476cf0c67fcbecf2014999bdb34107fa0045e906e8b0a5554b218ca9348d26940ec83b25409d68f0934925b255c436ed4d5098213a72f8da533e0d830bb6f3cadb6012a69a56197711f68f1f11e65fe0f2fabcb7ad43eb18e22ea9e0b0f4885b4cd4bc7f1b246d8042577fddf4ae2db0afa1542bbd3e743d2f6c49c97e545b61a89e6fc51d254e1d3f9"
    }
}
```

### Incorrect CHANGE
This collection divides itself further down into:
- JSON format errors
- no/random use case defined
- wrong values
**PROBLEM**: Doesn't work, need test data for it. (Tested on main - 24.01)

Example (Missing Field):
```json
{
    "changePublisherName":{
        "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr1faDzSg07x+5hvEDGzUzpSkedtQaq0CHJV8MZrRXXUVOQ21a0eBnoVMZLADuBISyW0gj6nJ9dtu+T+KFUxJKuDIIVfNPMqmehPqqWxv8qRsUQywaRBnWm4QIW2I8BdQINvvDULFO6nG3DknyzYku3HPA+TVt147opqWqTUPivkBuEJN/ANroAq1P9WlrjbyFSdqHtuPDavXaVwq8JZhxKqhE4w0aAGryE5HCDIT1hAq42G2CC5NNW3IaZVBBMqPn/tNCp0sQtUJiQZ19erolrcAxVIFd4Rv+YuMSpYKXuyFHPcUUjwLGyj7wq5mE9YRp+xnQ0RHLl3JSoyJeGAQCKD1M6d2mI1sBP/kqQS9xFWmvDbHG9XnGrYRAWFPlEln8gPF4WyhSqDyX7959gfhowGZJksZk9l9Ofbr9BWpOp65Aib4TQJXRgfeMkmDsYneF7e2p+4Watbbe7KBlvMgR6YIRq9OYbSGPAikdVet/j0A9SAKY0DZhq2FRlzG2RAiIV0GvI+j5aZs3d4ljjy6VVK/O3URKL4znOM6mRZUl0Fq7Jo5c0JDFgeXorGbqo8RHKeSmMHh8O37sj1V1p6AWgtJgu4cSkFPkxqUp7z9XHZo/KZaUAf8YfzTqQGThTS6MpqVczrKXYsdghwFAtBep+Ba+QKuYVVIpPbwgGRyCmsCAwEAAQ==",
        "fingerPrintPublicKey":"075966285278f8dbc92b49342ede3869b1a75cec",
        "publisherName":"real-factchecker",
        "newPublisherName": "checkey-factfredder",
        "signatureOnFingerPrintPublicKeyPublisherNameNewPublisherNameTimestampCHANGEFLAG":"8e20534defb6844f12b5942f73dde15ebd5e1ddeb77ddddda57fbc700cc984112d74c516560eb21374c4eabdcd717190f5a128309f668c9ba070d6dbe7f8ffea6251f1ee9877783ad61565354a095acf83382654c4078ab70ccc88b8f75eefc7f98dd38505cb7b30d49852d0b313faf483aef9af2a5a492dd6cfa52c0e59518f2f2cccdf82193433c56b545a79b6dc5f452eec4b2de01cb0168306ea4e0431277940fb4e977caf458295afe01e34a65934066aebc984c599ff2a6fa4dadd72b846f27199ada09b5aef74a13cbdb48c0fd9a1427f5bba747939ab06e64b9d4f090a67e7a3966ce28ea68b2177005c7d379079ab326347970c121804997c25337eb4677850f7684662ab3b588cb48c250e7c9649f7407380bb5e82d43438dba51cc7755dd894f6d2c9b7a3c73133522505903e7efb4b9b437bd9da6388ef66ef4c81e3096b0c0beca1f4b15bfc8c3237e12f00a7b58647d935cbe2b9c2b32923d4c36d8e18489ada5ead380858009424559949b1943cbd18fa192422d44699622629ccab2ebb935831a8dc7b837ce5106854e4f7b9cecdb325a09a26b03eed5dc4b6f0d071df2610137cc13ef678f926fa370f6821f02c251c41c7bcbccf23e25cf2800497c2768f89963fa84ee8a85d30d1ffc3173d926b732937bc78c55ef6f14c60e1e8a7c0776a5750afed436122829309c23034c5fcdf12bba589f6ea1c32"
    }
}
```

### Incorrect DELETE
This collection divides itself further down into:
- JSON format errors
- no/random use case defined
- wrong values
**PROBLEM**: Doesn't work. (Tested on main - 24.01)

Example (Remove 4 symbols of signature):
```json
{
    "deleteAccount":{
        "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr1faDzSg07x+5hvEDGzUzpSkedtQaq0CHJV8MZrRXXUVOQ21a0eBnoVMZLADuBISyW0gj6nJ9dtu+T+KFUxJKuDIIVfNPMqmehPqqWxv8qRsUQywaRBnWm4QIW2I8BdQINvvDULFO6nG3DknyzYku3HPA+TVt147opqWqTUPivkBuEJN/ANroAq1P9WlrjbyFSdqHtuPDavXaVwq8JZhxKqhE4w0aAGryE5HCDIT1hAq42G2CC5NNW3IaZVBBMqPn/tNCp0sQtUJiQZ19erolrcAxVIFd4Rv+YuMSpYKXuyFHPcUUjwLGyj7wq5mE9YRp+xnQ0RHLl3JSoyJeGAQCKD1M6d2mI1sBP/kqQS9xFWmvDbHG9XnGrYRAWFPlEln8gPF4WyhSqDyX7959gfhowGZJksZk9l9Ofbr9BWpOp65Aib4TQJXRgfeMkmDsYneF7e2p+4Watbbe7KBlvMgR6YIRq9OYbSGPAikdVet/j0A9SAKY0DZhq2FRlzG2RAiIV0GvI+j5aZs3d4ljjy6VVK/O3URKL4znOM6mRZUl0Fq7Jo5c0JDFgeXorGbqo8RHKeSmMHh8O37sj1V1p6AWgtJgu4cSkFPkxqUp7z9XHZo/KZaUAf8YfzTqQGThTS6MpqVczrKXYsdghwFAtBep+Ba+QKuYVVIpPbwgGRyCmsCAwEAAQ==",
        "fingerPrintPublicKey":"075966285278f8dbc92b49342ede3869b1a75cec",
        "publisherName":"real-factchecker",
        "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG":"534defb6844f12b5942f73dde15ebd5e1ddeb77ddddda57fbc700cc984112d74c516560eb21374c4eabdcd717190f5a128309f668c9ba070d6dbe7f8ffea6251f1ee9877783ad61565354a095acf83382654c4078ab70ccc88b8f75eefc7f98dd38505cb7b30d49852d0b313faf483aef9af2a5a492dd6cfa52c0e59518f2f2cccdf82193433c56b545a79b6dc5f452eec4b2de01cb0168306ea4e0431277940fb4e977caf458295afe01e34a65934066aebc984c599ff2a6fa4dadd72b846f27199ada09b5aef74a13cbdb48c0fd9a1427f5bba747939ab06e64b9d4f090a67e7a3966ce28ea68b2177005c7d379079ab326347970c121804997c25337eb4677850f7684662ab3b588cb48c250e7c9649f7407380bb5e82d43438dba51cc7755dd894f6d2c9b7a3c73133522505903e7efb4b9b437bd9da6388ef66ef4c81e3096b0c0beca1f4b15bfc8c3237e12f00a7b58647d935cbe2b9c2b32923d4c36d8e18489ada5ead380858009424559949b1943cbd18fa192422d44699622629ccab2ebb935831a8dc7b837ce5106854e4f7b9cecdb325a09a26b03eed5dc4b6f0d071df2610137cc13ef678f926fa370f6821f02c251c41c7bcbccf23e25cf2800497c2768f89963fa84ee8a85d30d1ffc3173d926b732937bc78c55ef6f14c60e1e8a7c0776a5750afed436122829309c23034c5fcdf12bba589f6ea1c32"
    }
}
```

## GET Requests
Get requests generally only test different formats and values of the URL.
#### Correct Factcheck
Get fact checks for a URL.
Example:
```
localhost:8080/factChecks/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93/1d3f4630d911fea226898a7a3116166b3a96b06f/
```

#### Correct Publisher
Get all publishers on the server.
Example:
```
localhost:8080/publishers/page/1
```

#### Correct Publisher_fact
Get all fact check publishers for a specific URLToCheckHash.
Example:
```
localhost:8080/publishers/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93/*
```
with following checks:
```javascript
pm.test("Data insertion successfull", function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData.publishersForSpecificLink[0].fingerPrintPublicKey).equals("1d3f4630d911fea226898a7a3116166b3a96b06f")
    pm.expect(jsonData.publishersForSpecificLink[0].publicKey).equals("MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqrp9b+gh7PQXOAQVnHbnPswXAX6/dZ3UYkU+KQ7TTPzp+pRudifRvqn7/cqx4zbAfDwf1beZEtjxK6KR16zxqPAQ5m0hEeboVDQk7zTUU8BlFEs3TfhwubK/OJSROyRGhpH+Cx9oMIJNDA9p3Pn74RrgkKwqEpkXUOAx/ld6U39gVxC2uhUMwtmHG1h305tWc4THVpz/nElazuqKtpC7H8mAJmfQcHV5uGm1JoLivKiCQR1l6L8JVjB5x9rINepfljAWvLMZxIqjhEppC3TW6+Gv3/6dxvwSvPrfN525MQOYEW2Cz8nq6r4lTqs5XX8dVXZ3Dqa+P8Vdg3zpU6pUfo8zavHOeGkJHiexS37fdMWGC1A/XkqTCEat5ycM5o/Kms1ox/Nza/tVi+Z2/+cZgGa9YIplaqxrWdJjCwAwJ0xAsCqz3hPTgCmP2LXwRzTrBhvrky6+d48Xcbeqst6Ut9RCNe+Aj/6nDnNBQvNt7oFvVM6Lhw6Ux9d462Mt3uF75doXIJbwczjW3IAYDHnBHbVd9V+feZNDm0IRWo3p9yINu/fIQEQKaMsSHxtxm8oTdwi/BVULhyaSXS3+gcRDMjdrB+u71ictb+iffdSX86e6d/60ouX6M1t/mdh7qFDNdMV9n7eE59Gy0jp/u9NekMkbVnvTUH9bcRAuF4o30zMCAwEAAQ==")
    pm.expect(jsonData.publishersForSpecificLink[0].publisherName).equals("power-factchecker")
    pm.expect(jsonData.publishersForSpecificLink[0].signatureOnPublicKeyPublisherName).equals("08f5e87f9ee6db7c6767791c9006537e3d358c578acc7d790f2b83450bd00f55c4727e49d66fee0de7de4afc262553ce65064846a7dcba37648d0c68442b773ece10be2afa37f53c171f469305b01acdd6d448fd8aec48ec6346651dfe2ed9b62815b0cd976e9331979019df1c3ef2af36177f8cb145be3fd56438e90fc309e1b16418eef317bbfdf67072427a8d3d564d8c0e050e445de25588ab3f1f3aa32fdd64c122892ba2dca2e5fccc836048c37bae3d2528be41a8fbb013e4a9f1a8bedbc8121878658ddfe8fe168e6f9661401cdb2f503356c1c340616573b5fe711b346f6d3ce2438bd3d976df1887e2b753ad82b1f6073961a1c4634e5836757e0e3b37385d2f304949e287354cf6c61a07382b9e3277341561d29d0e50764c55130d48e378b34b43932e20e4cbf3cc8738d612d00064dfda3f0dd1d0600292c436f8b4d92f28687b61d806e75da399aea9b19daff9763e2c6a078dc1e7fc31f4d8cbe0fe53d36cb75f92abca898ba410775592639a2bdd8b3512874432578e3205fb5e6f797206d9b85a6433d969363a932a87a856433f47d5e92f695ecee1c4566db9c5f6b928cb60655a7fd7b339941eec86205c69c69794066fe11919ae9e7c33d08f8de24c60dd2ed09e244a89799cd593035934684df5dab3f53cbb497fcbecef22cf8997ba027d0fd3475c3f47386bec06bad097ca2d11a8726ceeb17b69")
});
```

#### Correct Revoke
Get list of public keys whose signatures should not be trusted
Example:
```
localhost:8080/publishers/revokedPubKeys/
```
with following checks:
```javascript
pm.test("Data insertion successfull", function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData.revokedKeys.numberOfKeys).equals(2)
    pm.expect(jsonData.keyList[0].publicKey).equals("TODO")
    pm.expect(jsonData.keyList[0].fingerPrint).equals("TODO")
    pm.expect(jsonData.keyList[0].publisherName).equals("TODO")
    pm.expect(jsonData.keyList[0].signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG).equals("TODO")
});
```

#### Incorrect Factcheck
Example (wrong fingerprint, single symbol):
```
localhost:8080/factChecks/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93/sss/
```

#### Incorrect Publisher
Example (non existent page):
```
localhost:8080/publishers/page/-1
```

#### Incorrect Publisher_fact
Example (non existent fingerprint):
```
localhost:8080/publishers/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a9/*
```

#### Incorrect Revoke
This case doesnt exist.