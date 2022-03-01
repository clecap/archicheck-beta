# General Prerequisites
- Install Docker. Depending on your Docker installation/configuration, you might have to run the scripts containing `docker` commands (or any `docker` command) with `sudo`.
- Create the docker network, so the python container and the mongoDB container can communicate: `docker network create archicheck-network`.
- Build the image that the python web server is based on: `$ ./prepare_pymongo_base.sh`. **This is only required once** and serves the purpose of not re-installing the `pymongo` and `pycryptodome` libraries everytime the final image is rebuilt.
- Edit the credentials for the database container: copy `db.conf.template` to `db.conf` and change its values.

# Extra Windows Prerequisites
Install Git-Bash or Bash-for windows to be able to execute all files.
After following the General Prerequisites, copy `dbconf.tmp` to `dbconf.bat` and change its values to the same credentials as in `db.conf` (the file `db.conf` is also needed, `dbconf.bat` is required **additionally** on Windows).

# Usage
## Linux
- Start the mongoDB container: `$ ./run_mongo_container.sh -t`. The database **must** be started before the web server.
    - you can also start the database in persistent mode by using the `-p` flag: `$ ./run_mongo_container.sh -p`.
    - to view logs of that container ("attach"): `$ docker attach archicheck-DB`.
    - or to achieve both at once and attach right away: `. db.conf && docker run --name archicheck-DB --network archicheck-network -e MONGO_INITDB_ROOT_USERNAME="$dbusername" -e MONGO_INITDB_ROOT_PASSWORD="$dbpassword" -it --rm mongo:5.0`
    - to stop ´the container running in the background: `docker stop archicheck-DB`. When attached, simply `CTRL-C` to stop.
      - keep in mind that this will also delete the DB for containers started in `--temporary` mode.
    - for more information on the persistence options and export/import, see `$ ./run_mongo_container.sh -h`
- `$ ./run_webserver_container.sh` to build the final web server image and run the resulting container. For development convencience, this also copies the current version of `python-web-server.py` from the host to the image. CTRL-C to quit.

## Windows
- start `Serverstart.bat` (starts web server, DB and builds the server image).
- to stop the server: start `Serverstop.sh`
(currently the mongo container starts in permanent mode, if needed, to change this, change the `run_mongo_container.sh -p` in the Serverstart file to `run_mongo_container.sh -t` )

# Client call examples
- For now, the webserver conforms to the API defined in the [interface description](../specification-documentation/interface_description.md) except for the call `4. GET publishers/revokedPubKeys/`. There are *some* checks performed on the server yet whether the JSON payload is correct.

## Create an account and publish a fact check
You can publish a new fact check **after** having created an account on the server. This is necessary because the server expects valid signatures and therefor needs the publisher's public key.
- to create an example account:
```
curl -d '
  {"createAccount":{
    "publicKey":"MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqrp9b+gh7PQXOAQVnHbnPswXAX6/dZ3UYkU+KQ7TTPzp+pRudifRvqn7/cqx4zbAfDwf1beZEtjxK6KR16zxqPAQ5m0hEeboVDQk7zTUU8BlFEs3TfhwubK/OJSROyRGhpH+Cx9oMIJNDA9p3Pn74RrgkKwqEpkXUOAx/ld6U39gVxC2uhUMwtmHG1h305tWc4THVpz/nElazuqKtpC7H8mAJmfQcHV5uGm1JoLivKiCQR1l6L8JVjB5x9rINepfljAWvLMZxIqjhEppC3TW6+Gv3/6dxvwSvPrfN525MQOYEW2Cz8nq6r4lTqs5XX8dVXZ3Dqa+P8Vdg3zpU6pUfo8zavHOeGkJHiexS37fdMWGC1A/XkqTCEat5ycM5o/Kms1ox/Nza/tVi+Z2/+cZgGa9YIplaqxrWdJjCwAwJ0xAsCqz3hPTgCmP2LXwRzTrBhvrky6+d48Xcbeqst6Ut9RCNe+Aj/6nDnNBQvNt7oFvVM6Lhw6Ux9d462Mt3uF75doXIJbwczjW3IAYDHnBHbVd9V+feZNDm0IRWo3p9yINu/fIQEQKaMsSHxtxm8oTdwi/BVULhyaSXS3+gcRDMjdrB+u71ictb+iffdSX86e6d/60ouX6M1t/mdh7qFDNdMV9n7eE59Gy0jp/u9NekMkbVnvTUH9bcRAuF4o30zMCAwEAAQ==",
    "fingerPrintPublicKey":"1d3f4630d911fea226898a7a3116166b3a96b06f",
    "publisherName":"power-factchecker",
    "firstLogin":"Mon, 15 Nov 2021 14:06:44 GMT",
    "signatureOnPublicKeyPublisherName":"08f5e87f9ee6db7c6767791c9006537e3d358c578acc7d790f2b83450bd00f55c4727e49d66fee0de7de4afc262553ce65064846a7dcba37648d0c68442b773ece10be2afa37f53c171f469305b01acdd6d448fd8aec48ec6346651dfe2ed9b62815b0cd976e9331979019df1c3ef2af36177f8cb145be3fd56438e90fc309e1b16418eef317bbfdf67072427a8d3d564d8c0e050e445de25588ab3f1f3aa32fdd64c122892ba2dca2e5fccc836048c37bae3d2528be41a8fbb013e4a9f1a8bedbc8121878658ddfe8fe168e6f9661401cdb2f503356c1c340616573b5fe711b346f6d3ce2438bd3d976df1887e2b753ad82b1f6073961a1c4634e5836757e0e3b37385d2f304949e287354cf6c61a07382b9e3277341561d29d0e50764c55130d48e378b34b43932e20e4cbf3cc8738d612d00064dfda3f0dd1d0600292c436f8b4d92f28687b61d806e75da399aea9b19daff9763e2c6a078dc1e7fc31f4d8cbe0fe53d36cb75f92abca898ba410775592639a2bdd8b3512874432578e3205fb5e6f797206d9b85a6433d969363a932a87a856433f47d5e92f695ecee1c4566db9c5f6b928cb60655a7fd7b339941eec86205c69c69794066fe11919ae9e7c33d08f8de24c60dd2ed09e244a89799cd593035934684df5dab3f53cbb497fcbecef22cf8997ba027d0fd3475c3f47386bec06bad097ca2d11a8726ceeb17b69"
    }
  }' localhost:8080/postendpoint
```
(without the newlines, those have been added only for readability.)
- to publish the URL containing the fact check [](https://correctiv.org/faktencheck/2021/12/01/angebliches-tucholsky-gedicht-ueber-impfungen-stammt-von-satire-autor/) for the fact checked URL [](https://twitter.com/C_W_M_O/status/1464241776697520130):
```
curl -d '{"publishNewFactCheck":
  {
    "URLToCheckHash":"f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93",
    "fingerPrintPublicKey":"1d3f4630d911fea226898a7a3116166b3a96b06f",
    "URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/01/angebliches-tucholsky-gedicht-ueber-impfungen-stammt-von-satire-autor/",
    "timestamp":"Sat, 18 Dec 2021 13:10:44 GMT",
    "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"3ae94ad9210e7700eb9a300c6af8f76a85a68371cb91b2bbf88f91962c8647d122f6754feb25bd60a91f7321ff585277726de01a9aee2b95b8d5c4fe44219e0ed07e615fc9908bbd80572f46702ce6e618cbf187847fb3cce69976472403caca52e0914953065afe4a696484a1931080b33229d82015664f1b12106750c863e6a7318285222c6528adb5eeabd83fb31cb1606bf8cfb83eb45a57558ae807f7368bc067e6d1cbd0b6d0bec5165b88e515838c5458cab6eb3f432e1da618cb2d4e0ec75edb2ae0840e15b550c456d7f174ceb4cc10d490eebbdf9560b8fde5573ca342d5080246d353098290d51c67833dad76cd451a7b6ec5b3c7d6986e8ba8bdb0b1130dceb1b01551eac2ac7b6862d56eab7899da5eec155db757fa920ea2e24bd9ebcd63cda33f4f0ea716ba05fdbda3f5d972b62f2d2754242f11cc0aeaa337fda7c0cba03b096c8c7d9ee60420efe86f4c37ce1e28a1d099863f8676ed96fe6b7a4534e26d7fee0ca3c96df55f07fabc021ac6be0476cf0c67fcbecf2014999bdb34107fa0045e906e8b0a5554b218ca9348d26940ec83b25409d68f0934925b255c436ed4d5098213a72f8da533e0d830bb6f3cadb6012a69a56197711f68f1f11e65fe0f2fabcb7ad43eb18e22ea9e0b0f4885b4cd4bc7f1b246d8042577fddf4ae2db0afa1542bbd3e743d2f6c49c97e545b61a89e6fc51d254e1d3f9"
    }
  }' localhost:8080/postendpoint
```
- with `URLToCheckHash` being the SHA-512 checksum of the URL that is being fact-checked
- from the fact checker with the public key fingerprint `fingerPrintPublicKey`
- with the URL containing the fact check itself `URLwithFactCheck` 
- with the ISO 8601 (seconds-precision) formatted timestamp `timestamp` (acquired e.g. via ` $ date --iso-8601=seconds`) **TODO: still is RFC 5322 in the example**
- with the signature on the concatenation of `URLToCheckHash`, `fingerPrintPublicKey`, `URLwithFactCheck` and `timestamp` using the private key belonging to `fingerPrintPublicKey`

## Request the published fact check:


- GET all publishers who published fact checks for this URL: `$ curl localhost:8080/publishers/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93/*`
- GET this the fact check for this URL by `power-factchecker` by replacing the `publishers` endpoint with `factChecks` and `*` with their fingerPrintPublicKey like this: `$ curl localhost:8080/factChecks/f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93/1d3f4630d911fea226898a7a3116166b3a96b06f`

- This example is taken from the [example accounts](./exampleuser.sh) and [example fact checks](./examplefacts.sh). These script can be used to populate the server database with sample data:
```
./exampleuser.sh
./examplefacts.sh
```

For more information on the available API calls, consult the [interface description](../specification-documentation/interface_description.md).

