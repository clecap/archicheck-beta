General idea: specify client-server-API first, then replace server component with proxy, which relays requests to actual P2P-network.

# GET Requests

## 1. GET `factChecks/<URLToCheckHash>/<fingerPrintPublicKey>`

- **Use case**: Getting fact checks for a URL (or rather its hash value)
- Response: valid response or `ErrorResponse`, if resource does not exist.
- if the resource exists, the server increments the counter for the publisher with `<fingerPrintPublicKey>`
- since multiple fact checks can be published by one publisher for a single URLToCheckHash, the response consists of a **list of fact checks**
- Example valid response with one fact check:

```
{specificFactCheck:[
    {
        "URLwithFactCheck": "https://correctiv.org/faktencheck/2021/10/28/dieses-foto-von-bauernprotesten-ist-2019-entstanden-und-medien-berichteten-ueber-die-strassenblockade/",
        "timestamp":"2022-01-14T17:33:49+01:00"
        "signatureOnPublisherNameURLToCheckHashFingerPrintURLwithfactCheckTimestamp": "0x49333755436642352f7333655a6e6b", "publisherName":"Friedrich-factchecker"
    }]
    }
```

## 2. GET `publishers/<URLToCheckHash>/*`

- Purpose: get all available fact check publishers for a specific URLToCheckHash, that can then be individually requested with the 1st GET call.
- **Use case**: getting fact checks for a URL, "explicit-request-mode" - Reader clicks on plugin icon, which opens a list of fact-checks for this URL.
- Response: List of all fact checkers who published for this `<URLToCheckHash>` (public Key fingerPrint + signed publisherName) or `ErrorResponse`.
- Example Response:

```
{"publishersForSpecificLink":[
    {
        "fingerPrintPublicKey": "0xA999B7498D1A8DC473E53C92309F635DAD1B5517",
        "publicKey":"0982370495827034985203452",
        "publisherName": "pablo-publisher",
        "signatureOnPublicKeyPublisherName": "0x49333755436642352f7333655a6e6b"
    },
    {
        "fingerPrintPublicKey": "0x6a6d574c4d51695273506968686e6636",
        "publicKey":"982374927394827938570913750927305",
        "publisherName": "freddy-factchecker",
        "signatureOnPublicKeyPublisherName": "0x52125755436642352f73336556ab3d"
    }
 ]}
```

## 3. GET `publishers/page/<page-number>`

- Purpose: get an overview of which publishers are available on the server/network.
- **Use case:** subscribe to a fact checker.
  - Reader clicks on plugin icon, then the user clicks on 'subscribe to fact checker'-button which opens a list of the available fact checkers ("publisher").
- Possible responses:

  - if there are publishers on the requested page:
    - List of 10 or less publishers (publicKey + publisherName) sorted by the request counter, that is incremented in `GET factChecks/<URLToCheckHash>/<fingerPrintPublicKey>` requests, in descending order.
  - if the page number exceeds the amount of available publishers on the server:
    - `{"allPublishers": {"method": "GET", "status": "Error", "message": "No publishers available on page <page>."}}` with HTTP status `404`.

- Example:
  - request: `GET publishers/page/1`
  - response:
  ```
  {"allPublishers":{
      "status":"OK",
      "requestedPage":1,
      "availablePages":1,
      "pageEntries":2,
      "publisherList":
      [
      {"publicKey":"35234623463",
      "fingerPrintPublicKey:"239472398523984234098",
      "publisherName":"freddy-factchecker",
      "signatureOnPublicKeyPublisherName":"982347923847",
      "requestCounter":2342,
      "numberOfFactChecks":25,
      "firstLogin": "2022-01-14T17:33:49+01:00"},
      {"publicKey":"123124124",
      "fingerPrintPublicKey:"239472398523984234098",
      "publisherName":"pablo-publisher",
      "signatureOnPublicKeyPublisherName":"124124124124",
      "requestCounter":1337,
      "numberOfFactChecks":31,
      "firstLogin": "2022-01-12T17:33:49+01:00"}
      ]}}
  ```
  - attribute definitions:
    - `requestedPage`: (int) the page number that has been requested.
    - `availablePages`: (int) the number of the last page number, that still has entries. If the requested page number exceeds this value, the response will be an Error Response as defined above.
    - `pageEntries`: (int) the number of publisher entries on this page. Will never exceed the value of 10.
    - `publisherList`: the actual publisher data
    - `requestCounter` (int) how many times a fact check of this publisher has been retrieved from the server. Serves as popularity indicator.
    - the other attributes are defined in the "Keyword definition" section below.
    - `numberOfFactChecks`: how many fact checks this publisher has published so far.

## 4. GET `publishers/revokedPubKeys/`

- Purpose: get the list of public keys whose signatures should not be trusted anymore.
- **Use case:** Bootstrap a node.
- Example response:
  ```
  {"revokedKeys":
      "status":"Ok",
      "numberOfKeys":"2",
      "keyList":
      [
      {"publicKey":"35234623463",
      "fingerPrint":"124124124124",
      "publisherName":"freddy-factchecker",
      "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG":"982347923847"
      },
      {"publicKey":"53212355325",
      "fingerPrint":"6423473235",
      "publisherName":"pablo-publisher",
      "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG":"5734135263354"
      },
      ]}
  ```

# POST Requests

All POST-Requests should be addressed to the endpoint `/postendpoint`.

## 1. Use case "publish single fact check"

- Example payload:

```
    {"publishNewFactCheck":
    {"URLToCheckHash":"faceBookLinkHash",
    "fingerPrintPublicKey":"9823475983475",
    "URLwithFactCheck":"correctivLink",
    "timestamp":"2022-01-14T17:33:49+01:00",
    "signatureOnPublisherNameURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"982347923847"}}
```

- Response: (_checks signature..._) -> "Ok" | `ErrorResponse`

## 2. Use case "delete fact check"

- Example payload:

```
{"deleteFactCheck":
    {"publicKey":"f1a4ce1Boo52k525Li5n2k1H25as5h",
    "fingerPrintPublicKey":"f152561126124",
    "URLToCheckHash":"f152561126124",
    "URLwithFactCheck":"falscherCorrectivLink",
    "signatureOnPublicKeyPublisherNameURLToCheckHashDELETEFLAG":"626347923847234234"}
}
```

## 3. Use case "create Account"

- Example payload:

```
{"createAccount":
        {"publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArVVVa3jkDi5cz1i5YliyWlU7Q62BWvX4Ifi7z9lvmhUpGKh9WJMSIrmdlBYrxPNc3kr2tABDMULpFyqY5ac1p98Utsz3F4n6oyZ0eHJVSUmsVJut124tQXFgMmFt7axgBtBFubirBoJFlqzTEUUuu+dMqocpmicE2ZWZkw1iX4iM671LULvn4z0c5w1WI65cnzvi/po/nqv9OxKrbjDOECB/CBL5aLKc6NoEbptOt2ZQrcMkkJq9aS7T/R90hMSN+8CHKjOdmPcDehNkFeT8MuSFM7twcivSmJnDRIkNHmhJ++ttOJ04EzO++2GGFDqAhqYXcx+RJ/vcdRLawXiA+fKfboxTIYfFsrAXQ8RZA4xGVYd2ZaB/vO880TZgCm3euQFQpzwSVr/k6z7jr+r21QV1jiCwOy+A7imU/v62SMhp8jsBwK786LPXeLmZ/VGw2oquInrNTzdDgs/PcI65YOs886xYlCeg5nzsxrawZwHj+251SAuzuWLWg7ONkBX6fmYSnDJmPryJwjjyu5C3aaUerijmB42DYgHCH/9394Bmw4JJ9qempYmLmSl34zDB2DgNCkgx52QxH19QWfglxiOlupGLmSPiNOtVWiuhPuYZcqGKM4qIWMeYK6Lp2onu3a2YSNqQw0a5Ckh2QBsQ0uQMuc1SP5BXEJQdfji+8wUCAwEAAQ==",
        "fingerPrintPublicKey":"f146dfff8ba2cc60aec546a4b0ab6ac66f53fb50",
        "publisherName":"freddy-factchecker",
        "firstLogin": "Fri, 17 Dec 2021 12:10:44 +0100",
        "signatureOnPublicKeyPublisherName":"4b6b68e2c2faa393cf35267e89ab50e135dc811d6f432cd925bed1331d4ecd009742fe8556fbb76c9e3929468bebaa563f993c34deb6ec5e144cb082b48bad870c49d3ecb236013fab276fd23692d865508cbd77c25feec801fbfa949e70c334d12d93daeca5053ac815924d034a1179b44c160bde68f2a6c9a38b2756539e7a19c7b41b969c2e6188f6ea36563ccff9bbe01fca8c0bb1e5b5d7b80f14490ba32a54abae66008cc0a3719a99c7e858f531f5db005f9f87494710625395e4a33b0fd139a54d2c6967e9ef3290f0db5b526c65365021767fd5de7f486f11127582d5a9349fa7a04c264a30caf06af9c14ff5aa4865028e5276e4a1604d9565724ff2a99c8d43b19df95e5859aea203bc9e56552a11db96794a0786200cb9b7870a9d180954ee77e689b23c4fa53b252ed5fc9c63ce38ba89429a236c0c28cda5b55d2709ef5b858c6b0a1543fbe7ca44c21517485386edac864f6f5353820a0dd6939fe253f42f19c0ccf9547404224707cf8611a79284a70d98ac8e5d3d2e9bcf39c291ea38c5025baff976e8ab6cd47d9ab2e00dd6ae89f4e29014131a9e10c348cecf1e7d9ac66e67d90c492862191b28c7245d049ae48268a274e889b68ad2ac395b68d3f62516eb32142569f914588f7c2f7f8405d711a045068e6570114a0e1cfc537a61303950c8cbf19529800f824658b92b26ee9b68e858c5470cc19b"
        }}
```

- Possible Responses:
  - `{"createAccount": {"method": "POST", "status": "OK", "message": "Account created."}}`
  - `{"createAccount": {"method": "POST", "status": "Error", "message": "Public key already exists."}}`
  - `{"createAccount": {"method": "POST", "status": "Error", "message": "Invalid signature 'foo' for data 'bar'."}}`

## 4. Use case "delete Account"
Can be called to delete the client's account in the server's database. If the `signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG` is valid, the server deletes the `publicKey`'s associated record from its database.

**Important**: However, the server does **not** delete the associated fact checks published with this public key. Instead, the client **must** use the API's 2. POST request "delete fact check" to delete their own published fact checks. The reason is that in a later P2P network, all fact checks will be distributed across different nodes and it will take a long time to call all those nodes to delete the fact checks. This work should rather be done by the client node than the server node.

- Example payload:
```
{"deleteAccount":
    {"publicKey":"f1a4ce1Boo52k525Li5n2k1H25as5h",
    "fingerPrintPublicKey":"f152561126124",
    "publisherName":"freddy-factchecker",
    "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG":"626347923847234234"}
}
```

- Possible Responses:
    - `{"deleteAccount": {"method": "POST", "status": "OK", "message": "Successfully deleted publisher: <publisher-representation>"}}`
    - `{"deleteAccount": {"method": "POST", "status": "Error", "message": "publisher does not exist: cannot delete."}}`
    - `{"deleteAccount": {"method": "POST", "status": "Error", "message": "Invalid signature '<signature>' for data '<data>'"}}`
    - `{"deleteAccount": {"method": "POST", "status": "Error", "message": "JSON is not wellformed."}}`
    


## 5. Use case "search Publisher"

- **Purpose**: the user can search for a publisher by their `publisherName` or `fingerPrint`
- Only **exact matches** (either publisherName or fingerPrint) will be found.
- there can be multiple result for search by publisherName, but **at most one** result by fingerprint (because they are unique in the system)
- expected HTTP status codes in response: even if a search term yields no results, the response status code will be 200 (OK)
- expected server response is either valid (see the two examples below) or an `ErrorResponse`:

```
{
    "searchPublisher": {
    "method":"POST",
    "status":"Error",
    "message":"<Error message>"
    }
}
```

### Example 1: Search term is a fingerprint

- Request:

```
{"searchPublisher":
    {"searchTerm":"952c45ccd94103c5dc52630c9704b06538c7b558",
    "timestamp":"2022-01-14T17:33:49+01:00"}
    }
```

- Response

```
    {"searchPublishersResult":
        {
            "status":"OK",
            "searchTerm":"952c45ccd94103c5dc52630c9704b06538c7b558",
            "resultsByPublisherNameAmount":0,
            "hasResultByFingerPrint":true,
            "resultByFingerPrint":{
                "publicKey":"35234623463",
                "fingerPrintPublicKey":"952c45ccd94103c5dc52630c9704b06538c7b558",
                "publisherName":"freddy-factchecker",
                "signatureOnPublicKeyPublisherName":"982347923847",
                "requestCounter":2342,
                "numberOfFactChecks":25,
                "firstLogin": "2022-01-14T17:33:49+01:00"
            },
            "resultsByPublisherName":[]
        }
    }
```

### Example 2: Search term is a publisherName

- Request:

```
{"searchPublisher":
    {"searchTerm":"freddy-factchecker",
    "timestamp":"2022-01-14T17:33:49+01:00"}
    }
```

- Response (two publishers have chosen the same name here):

```
    {"searchPublishersResult":
        {
            "status":"OK",
            "searchTerm":"freddy-factchecker",
            "resultsByPublisherNameAmount":2,
            "hasResultByFingerPrint":false,
            "resultByFingerPrint":null,
            "resultsByPublisherName":[
                {
                    "publicKey":"35234623463",
                    "fingerPrintPublicKey":"952c45ccd94103c5dc52630c9704b06538c7b558",
                    "publisherName":"freddy-factchecker",
                    "signatureOnPublicKeyPublisherName":"982347923847",
                    "requestCounter":2342,
                    "numberOfFactChecks":25,
                    "firstLogin": "2022-01-14T17:33:49+01:00"
                },
                {
                    "publicKey":"02983450298345",
                    "fingerPrintPublicKey":"2039457029384502983457575893020329847",
                    "publisherName":"freddy-factchecker",
                    "signatureOnPublicKeyPublisherName":"029384570238945",
                    "requestCounter":301,
                    "numberOfFactChecks":2,
                    "firstLogin": "2021-12-01T13:22:27+01:00"
                }
            ]
        }
    }
```

## 6. Use case "delete DB"

- **Only for testing purpose.**
- The entire DB can be deleted by sending an empty payload to the endpoint `/postendpoint/deleteDB`

# Keyword definition

- **publicKey**: required for the verification of the publisher of the fact checks. This is the base64 encoded RSA public key without the `-----BEGIN PUBLIC KEY-----` padding and without newlines.

- **signatureOnPublicKeyPublisherName**: is the signature on the SHA-512 hash of the concatenation of public key in base64 encoding of a user and his chosen publisherName, so that it can be proven that this publisherName is really the right one for this public key. This signature's bytes must be **encoded as hex string** for transmission.

- **signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp**: is the signature to prove a fact check's integrity. The signature is made over the SHA512 hash of the concatenation of `URLToCheckHash`, `fingerPrintPublicKey`, `URLwithfactCheck` and `timestamp`. This signature's bytes must be **encoded as hex string** for transmission.
- **signatureOnURLToCheckHashFingerPrintPublisherName** signature on the attributes contained in the name, as above.

- **signatureOnFingerPrintPublicKeyPublisherNameNewPublisherNameTimestampCHANGEFLAG**: is the signature to prove one owns the account and is entitled to change its publisherName. The signature is made over the fingerPrint of the public Key, old and new publishernames aswell as the current time that also has to be included in the request and a CHANGEFLAG which is explained further down.

- **fingerPrintPublicKey**: is the fingerprint of a public key. That is, the SHA-1 hash value of the public key (in base64 format, as received from front end, not the key bytes themselves). The fingerPrintPublicKey is used to identify a public key without having to transmit the whole key.

- **URLToCheckHash**: is the hash value of a URL that is fact checked. The hash of it is used for privacy reasons.

- **URLwithFactCheck**: is the URL at which the actual fact check is located (that what's in the URL, will be checked). This is not a hash here, because you need the actual URL to call it up later.

- **publishers**: is the path to the publisher directory on the server, which is used to access all fact checks published _by a specific publisher_.

- **factChecks**: is the resource where factChecks can be accessed - either all fact checks by arbitrary publishers for a specific `URLToCheckHash` or only for a specific `URLToCheckHash` by the publisher specified by `fingerPrintPublicKey`.

- **timestamp**: timestamp when the factCheck was initially published (i.e. "sent to the server"), in `ISO 8601` format

- **DELETEFLAG**: literally the string "DELETEFLAG" to prove that the owner of the private Key (i.e. the publisher) approved that this fact check should be deleted.


---

- Character Encoding by default: UTF-8.

* Hashfunction to use: SHA-1 for the fingerprint (which is made of the base64 encoded public key, not the bytes themselves!), SHA-512 for everything else (including hashing the data before signing it)
* signature encoding: hex string of the signature bytes.
* Keypair format: RSA 4096 via `PKCS1_v1_5`
* timestamp format `ISO 8601`
