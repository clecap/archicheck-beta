# Structure of the Frontend

## Introduction

We will realize Archicheck as a Chrome Extension.
For this purpose we use _Node.js_ and _webpack_ to include external libraries.

## Prerequisites

- install _nvm_ and _Node.js_ on your OS
- node-version: v14.17.0
- npm-version: 8.1.4
- clone the repo from github
- run the following commands on your console:

  1.  Initialize _npm_ in your project at the `/frontend` folder with: `$ npm init`
  2.  Install all dependencies with: `$ npm install`
      (You can take a look at the `package.json` file to see all _Node.js_ libraries that we are using)

## Usage

Now you can run two different scripts:

1.  For development: `$ npm run dev` or `$ npm run dev_windows`
    (Reloads the Chrome Extension after you save any change)
2.  If you only need one image run: `$ npm run build` or `$ npm run build_windows`

- After you run `$ npm run dev` or `$ npm run build` for the first time _webpack_ will create a `/dist` folder located at `frontend/dist`. If you unpack this folder in your chrome browser at `chrome://extensions` you can use and/or develop the extension.
  Note: To unpack the folder your Chrome Browser must be in developer mode

## Structure of the Extension

```flow
+-------------------------------------------------------------+                   +------------------------+
|Frontend (Browser Extension)                                 |                   | Backend (Webserver)    |
|                                                             |                   |                        |
| +---------------------------------------------------------+ |                   |                        |
| | ui                                                      | |                   |                        |
| |                                                         | |                   |                        |
| | - all html/css files                                    | |                   |                        |
| | - manifest.json to define the extension                 | |                   |                        |
| |                                                         | |                   |                        |
| +---------------------------------------------------------+ |                   |                        |
| +---------------------------------------------------------+ |  req              |                        |
| | js                                                      +-+------------------->                        |
| |                                                         | |                   |                        |
| | - all javascript files                                  | |                   |                        |
| | - background script (service_worker) of the extension   | |  rsp              |                        |
| | - signing and verifying of the signatures               <-+-------------------+                        |
| | - generating rsa keypair                                | |                   |                        |
| |                                                         | |                   |                        |
| +---------------------------------------------------------+ |                   |                        |
| +---------------------------------------------------------+ |                   +------------------------+
| | dist                                                    | |
| |                                                         | |
| | - build image of the extension                          | |
| | - can be executed by the browser                        | |
| | - Note: the dist folder isnt uploaded to git take a look| |
| |         at the README.md to build it                    | |
| |                                                         | |
| |                                                         | |
| +---------------------------------------------------------+ |
|   webpack.config                                            |
|   package.json                                              |
|   node-modules folder (excluded from git)                   |
|   README.md                                                 |
|                                                             |
+-------------------------------------------------------------+
```

All data requests to the webserver (URLs, fact-checker, ..) are handled by the `background.js` script which is defined as a service_worker in the manifest.

## Add new files to the project

- **html-files** Put your new html-file in the `frontend/ui` directory. The html-files are just copied to the `/dist` folder during the build process
- **js-files** There is a little bit more to do:
  1. Go into the `webpack.config.js` file and add your new javascript file to the entry.
  2. If you want to use some more node libraries install them via `npm install --save-dev [name of the library]`

## Crypto

Every data that is 'produced' by the extension (e. g. a published factcheck) must be signed with a cryptographic key.
On the otherside the extension has to check all signatures that it receives from the webserver.

For the signing/verifying of signatures the Key Pair we are using is: _RSASSA-PKCS1-v1_5 4096_ and the hash: _SHA-512_.

The Public Key is currently exported as Base64 encoded and the signature as hex values.

To see where we are using the keys take at look at our [interface_description.md](../specification-documentation/interface_description.md)
