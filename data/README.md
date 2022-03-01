# Specifications for mongoDB data

## factcheck relations

for displaying the factchecks on a website we need to store those relations and we do that in the following way:

### needed information:

- [1] **URLtoCheckHash** website that is to be fact checked  (special hash of the website to prevent search errors)
- [2] **fingerPrintPublicKey** fingerprint of the publicKey representing the publisher (\_id in publisher data)
- [3] website of the fact **URLwithFactCheck**
- [4] **timestamp** of the publication
- [5] **signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp** signature over concatenation of [1], [2], [3] and [4]

### how is this stored

to prevent duplicates we are going to concatenate [1] + [2] + [3] and store all the information under this value as \_id:

```
db.factChecks.insertOne(

_id: concatenation of [1], [2] and [3],
URLtoCheckHash: [1],
fingerPrintPublicKey: [2],
URLwithFactCheck: [3],
timestamp: [4],
signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp: [5]

)
```

## publisher data

for approving login and identification purposes we store publisher data and we do that in the following way:

### needed information:

- [1] **fingerPrintPublicKey** representing the publisher
- [2] **publicKey** of the user
- [3] **publisherName**
- [4] timestamp of **firstLogin**
- [5] **signatureOnPublicKeyPublisherName** over public key and publisher name
- [6] **requestCounter** (64bit signed integer / long) how often a fact check from this publisher has been requested. Maximum value is 9223372036854775807.

### how is this stored

to prevent duplicates we use the fingerprint as \_id:
```
db.publishers.insertOne(

_id: [1],
publicKey: [2],
publisherName: [3],
firstLogin: [4],
signature: [5],
requestCounter: [6]

)
```
