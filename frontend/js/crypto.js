/**
 * @author mlr-f & Finn Kohlscheen
 */
// file for all crypto functions

import { Base64 } from "js-base64";
import Localbase from "localbase";
let db = new Localbase("db");

// signs data with private Key and returns it as hex
export async function sign(data) {
  // encode data in a form we can use for sign operation
  let enc = new TextEncoder();
  let encoded = enc.encode(data);

  let result = await db.collection("keys").doc({ id: 1 }).get();
  let signature = await crypto.subtle.sign(
    { name: "RSASSA-PKCS1-v1_5", saltLength: 32 },
    result.keys.privateKey,
    encoded
  );
  
  let signature_as_hex = buf2hex(signature);
  return signature_as_hex;
  
}

// verifies data+signature with a given publicKey 
// (key must be a cryptoKey object)
export async function verify(publicKey, data, signature) {
  // encode data in a form we can use for verify operation
  let enc = new TextEncoder();
  let encoded_data = enc.encode(data);
  let encoded_signature = hex2buf(signature)
  
  let isVerified = await crypto.subtle.verify(
    { name: "RSASSA-PKCS1-v1_5", saltLength: 32 },
    publicKey,
    encoded_signature,
    encoded_data
  );
  
  return isVerified; // true or false
}

// returns public key in PEM format
export async function getPublicKey() {
  let result = await db.collection("keys").doc({ id: 1 }).get();

  let exported = await crypto.subtle.exportKey("spki", result.keys.publicKey);
  const key_as_string = String.fromCharCode.apply(
    null,
    new Uint8Array(exported)
  );
  const exportedAsBase64 = Base64.btoa(key_as_string);

  return exportedAsBase64;
}

// imports a publicKey in PEM Format to cryptoKey Object
export async function importPublicKey(publicKey) {
  const decodedPublicKey = Base64.atob(publicKey)
  const keyInArrayBuffer = str2ab(decodedPublicKey)

  let importedKey = await crypto.subtle.importKey(
    "spki",
    keyInArrayBuffer,
    {
        name: "RSASSA-PKCS1-v1_5",
        hash: "SHA-512"
    },
    true,
    ["verify"]
  )
  
  return importedKey
}

// generate a sign/verify key pair and save it in IndexedDB
export async function makeAndSaveKeys() {
  var crypto_keys = await crypto.subtle.generateKey(
    {
      name: "RSASSA-PKCS1-v1_5",
      modulusLength: 4096, // can be 1024, 2048, or 4096
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
      hash: { name: "SHA-512" }, // can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
    },
    false, // whether the key is extractable (i.e. can be used in exportKey)
    ["sign", "verify"] // must be ["encrypt", "decrypt"] or ["sign", "verify"]
  );
  db.collection("keys").add({ id: 1, keys: crypto_keys });
}

function buf2hex(buffer) {
  // buffer is an ArrayBuffer
  return [...new Uint8Array(buffer)]
    .map((x) => x.toString(16).padStart(2, "0"))
    .join("");
}

function hex2buf(hexString) {
    // remove the leading 0x
    hexString = hexString.replace(/^0x/, '');
    
    // ensure even number of characters
    if (hexString.length % 2 != 0) {
        console.log('WARNING: expecting an even number of characters in the hexString');
    }
    
    // check for some non-hex characters
    var bad = hexString.match(/[G-Z\s]/i);
    if (bad) {
        console.log('WARNING: found non-hex characters', bad);    
    }
    
    // split the string into pairs of octets
    var pairs = hexString.match(/[\dA-F]{2}/gi);
    
    // convert the octets to integers
    var integers = pairs.map(function(s) {
        return parseInt(s, 16);
    });
    
    var array = new Uint8Array(integers);
    
    return array.buffer;
}

// from https://developers.google.com/web/updates/2012/06/How-to-convert-ArrayBuffer-to-and-from-String
function str2ab(str) {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

/*** some other helpful functions  ***/
export const is_url = (str) => {
  const regexp =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
    if (regexp.test(str)){
          return true;
    }
    else{
      return false;
    }
}
