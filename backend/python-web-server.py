#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from math import ceil
from collections import OrderedDict
import pymongo
import json
# ObjectId from mongoDB is not JSON-serializable, for that use json_util.dumps() intead of json.dumps():
from bson import json_util
import copy
import os

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA
from base64 import b64encode, b64decode
import backendFunctions as df

HOST_NAME = "0.0.0.0"
HOST_PORT = 80
POST_END_POINT = "/postendpoint"

EXPECTED_ATTRIBUTES_CREATE_ACCOUNT = ["publicKey", "fingerPrintPublicKey", "publisherName", "firstLogin",
                                      "signatureOnPublicKeyPublisherName"]
EXPECTED_ATTRIBUTES_DELETE_ACCOUNT = ["publicKey", "fingerPrintPublicKey", "publisherName",
                                      "signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG"]
EXPECTED_ATTRIBUTES_RENAME_ACCOUNT = ["publicKey", "fingerPrintPublicKey", "publisherName", "newPublisherName",
                                      "timestamp",
                                      "signatureOnFingerPrintPublicKeyPublisherNameNewPublisherNameTimestampCHANGEFLAG"]
EXPECTED_ATTRIBUTES_SEARCH_PUBLISHER = ["searchTerm", "timestamp"]
EXPECTED_ATTRIBUTES_PUBLISHNEWFACTCHECK = ["URLToCheckHash", "fingerPrintPublicKey", "URLwithFactCheck", "timestamp",
                                           "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp"]
EXPECTED_ATTRIBUTES_DELETEFACTCHECK = ["publicKey", "fingerPrintPublicKey", "URLToCheckHash", "URLwithFactCheck",
                                       "signatureOnPublicKeyPublisherNameURLToCheckHashDELETEFLAG"]
MAX_ENTRIES_PER_PAGE = 10

# Read DB credentials from environment variables and set up database connection:
print("Connecting to database as user '" + os.environ["dbusername"] + "'.")
DB_CONN_STR = "mongodb://" + os.environ["dbusername"] + ":" + os.environ["dbpassword"] + "@archicheck-DB"
db_client = pymongo.MongoClient(DB_CONN_STR, serverSelectionTimeoutMS=5000)
print("Database info:")
try:
    print(db_client.server_info())
except:
    print("Unable to connect to mongoDB.")

db = db_client.get_database("archicheckDB")

try:
    fact_coll = db.create_collection("factChecks")
    publisher_coll = db.create_collection("publishers")
except Exception as e:
    print(e)
    fact_coll = db.get_collection("factChecks")
    publisher_coll = db.get_collection("publishers")

validator_expression = { '$jsonSchema':
    {
             "bsonType": "object",
             "required": ["URLToCheckHash", "fingerPrintPublicKey", "URLwithFactCheck", "timestamp", "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp"],
             "properties": {
                 "URLToCheckHash": {
                     "bsonType"     : "string",
                     #"pattern"      : "^[A-Fa-f0-9]{128}$",
                     "description"  : "must be a string and match the regular expression pattern"
                 },
                 "fingerPrintPublicKey": {
                     "bsonType"     : "string",
                     "description"  : "must be a string"
                 },
                 "URLwithFactCheck": {
                     "bsonType"     : "string",
                     "description"  : "must be a string"
                 },
                 "timestamp": {
                     "bsonType"     : "string",
                     #"pattern"      : "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$",
                     "description"  : "can only be a timestamp"
                 },
                 "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp": {
                     "bsonType"     : "string",
                     "description"  : "must be a string"
                 }
             }
    }
}
#cmd = OrderedDict([ ('collMod', "factChecks"),
                    #('validator', validator_expression),
                    #('validationLevel', 'moderate')
                    #('validationAction', 'warn'])

db.command("collMod", "factChecks", validator=validator_expression, validationLevel='moderate')
#db.command("collstats", "factChecks")

print("Validator loaded")

# param dictionary: record json as dict
# return: pymongo.results.InsertOneResult
def db_insert_one(coll, dictionary):
    return coll.insert_one(dictionary)


# param  coll: the mongoDB collection that will be searched
# param  db_filter: dict
# return: iterable cursor on result set
def db_find(coll, db_filter=None):
    return coll.find(db_filter)


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def status_response(method, use_case, status, message=""):
    """
    Constructs frequently used JSON responses.

    Parameters:
    method (```str```): either GET or POST.
    use_case (```str```): the usecase of the preceding request, might be "unknown".
    status (```str```): either "Error" or "OK".

    Returns:
    ```str```: JSON string ready to be sent to client.
    """
    return json.dumps({use_case: {"method": method, "status": status, "message": message}}) + "\n"


def ok_response(method, use_case, message):
    return status_response(method, use_case, "OK", message)


def error_response(method, use_case, message):
    return status_response(method, use_case, "Error", message)


# helper functions
def stringify_DB(cursor, attributes, isList=True):
    records = ""
    reached_end = False
    while (not reached_end):
        try:
            records += str(cursor.next())
            records += "\n"
        except StopIteration:
            reached_end = True
    records = records.replace("(", "").replace(")", "").replace("ObjectId", "").replace("'", '"').replace("_", "")
    results_list_string = records.split("\n")
    results_list_string.pop()
    results_list_dict = []
    for r in results_list_string:
        results_list_dict.append(json.loads(r))
    pop_list = []
    if len(attributes) > 0:
        for i in results_list_dict:
            for k in i:
                if k in i and k not in attributes:
                    pop_list.append(k)
            for n in pop_list:
                i.pop(n)
            pop_list = []
    if isList:
        result = "["
    else:
        result = ""
    for s in results_list_dict:
        result += json.dumps(s) + ","
    result = result[:-1]
    if isList:
        result += "]"
    return result


def get_dict_list(dict):
    list = []
    for key in dict.keys():
        list.append(key)
    return list


def check_signature(pub_key_b64, signature_bytes_hexstring, message_string):
    """
    Verifies the given signature of the SHA512 hash of the given message_string with the given key.

    Parameters:
    pub_key_b64 (```str```): the public key as base64 encoded string without padding.
    signature_bytes_hexstring (```str```): the bytes for the signature encoded as hex-string.
        This is received in this format from front end.
    message_string (```str```): the data that has been signed. More specifically: its SHA512 hash has been signed.

    Raises Exception: if the signature is invalid or the key or the signature cannot be read.

    """
    print("Checking signature...")
    pub_key = RSA.importKey(b64decode(pub_key_b64))
    verifier = PKCS1_v1_5.new(pub_key)
    sig_bytes = bytes(bytearray().fromhex(signature_bytes_hexstring))
    # signature is not made for the raw message but its hash:
    message_hash = SHA512.new(bytes(message_string, 'utf-8'))
    if (verifier.verify(message_hash, sig_bytes)):
        print("Valid signature.")
    else:
        print("Invalid signature.")
        raise Exception("Invalid signature '%s' for data '%s'" % (signature_bytes_hexstring, message_string))


def check_fingerprint(pub_key_b64: str, fingerprint: str) -> None:
    """
    Computes the SHA-1 fingerprint of given public key and compares it to given fingerprint.

    Parameters:
    pub_key_b64 (```str```): the public key as base64 encoded string without padding.
    fingerprint (```str```): the SHA-1 fingerprint whose correctness should be verified.
        This is received in this format from front end.
    Returns:
    ```None```: if the provided fingerprint matches the provided public key's correct fingerprint.

    Raises Exception: if the fingerprint is not equal to the expected ('correct') fingerprint of this public key
        or the key or the public key cannot be read.
    """
    print("Checking fingerprint...")
    fingerprint_hash = SHA.new(bytes(pub_key_b64, "utf-8"))
    correct_fingerprint_hexstr = fingerprint_hash.hexdigest()
    print("Expected correct fingerprint: " + str(correct_fingerprint_hexstr))

    if (correct_fingerprint_hexstr == fingerprint):
        print("Fingerprint correct.")
    else:
        exception_msg = "Invalid fingerprint '%s' for public key '%s'.\nShould be '%s'." % (
            fingerprint, pub_key_b64, correct_fingerprint_hexstr)
        print(exception_msg)
        raise Exception(exception_msg)


def payload_is_correct(payload_copy, expected_attributes):
    correct_payload = expected_attributes.copy()
    payload_attributes = get_dict_list(payload_copy)
    for attribute in payload_attributes:
        if attribute in correct_payload:
            correct_payload.remove(attribute)
        else:
            print("Malformed JSON - forbidden attribute: '%s'." % attribute)
            return False
    if correct_payload == []:
        return True
    else:
        print("Malformed JSON - missing attribute:\n" + str(correct_payload))
        return False


# iterates over entries under cursor and collects them to a list of dicts.
# a limit for returned entries can be set via limit parameter
def collect_entries(cursor: pymongo.cursor.Cursor, limit: int = None) -> list:
    result_list = []
    record = next(cursor, None)
    if (limit == None):
        while (record):
            result_list.append(record)
            record = next(cursor, None)
    elif (limit):
        counter = 1
        while (record and (counter <= limit)):
            result_list.append(record)
            record = next(cursor, None)
            counter += 1
    return result_list


def enrich_publisher_info(publisher: dict) -> dict:
    """
    Add the amount of published fact checks to the provided publisher,

    Parameters:
    publisher (```dict```): one result dict from the collection `publisher_coll`.

    Returns:
    ```dict```: a copied dict, with added number of published fact checks and
        renamed the `_id` attribute to `fingerPrintPublicKey` as demanded in API.
    """
    publisher_copy = publisher.copy()
    number_of_fact_checks = fact_coll.count_documents({"fingerPrintPublicKey": publisher["_id"]})
    publisher_copy["numberOfFactChecks"] = number_of_fact_checks

    # fingerprint is in DB as attribute '_id', change that in sent payload:
    publisher_copy["fingerPrintPublicKey"] = publisher["_id"]
    publisher_copy.pop("_id")
    return publisher_copy

def send_http_response(self, status_code: int, body_str: str) -> None:
    """
    Sends the given parameters as HTTP response. Content-type will be set constantly
    to 'application/json') and encoding will be utf-8.

    Parameters:
    self: instance of Handler
    status_code (```int```): HTTP status code to be sent
    body_str(```str```): the body of the HTTP response.

    Returns:
    ```None```
    """
    self.send_response(status_code)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(bytes(body_str, "utf-8"))

# Switchcase for every Post Request
def process_POST_request(payload_string, self):
    payload = json.loads(payload_string)
    use_case = next(iter(payload))
    if df.is_valid_payload(payload) == "":
        if use_case == "publishNewFactCheck":
            payload = payload[use_case]
            if payload_is_correct(payload, EXPECTED_ATTRIBUTES_PUBLISHNEWFACTCHECK):

                # Check if this fact check this this URL hash already exists:
                cursor = db_find(fact_coll, {"fingerPrintPublicKey": payload["fingerPrintPublicKey"],
                                             "URLToCheckHash": payload["URLToCheckHash"],
                                             "URLwithFactCheck": payload["URLwithFactCheck"]})
                exists_fact_check = next(cursor, None)
                if (exists_fact_check):
                    send_http_response(self, 400, error_response("POST", "publishNewFactCheck",
                        "There is already a DB entry with this fact check URL and publisher/URL"))
                else:
                    # insert new fact check:
                    try:
                        cursor = publisher_coll.find({"_id": payload["fingerPrintPublicKey"]})
                        try:
                            publisher_record = cursor.next()
                        except StopIteration:
                            raise StopIteration("Signed with unknown public key - publisher does not exist.")
                        pub_key = publisher_record["publicKey"]
                        sig = payload["signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp"]
                        signed_data = payload["URLToCheckHash"] + payload["fingerPrintPublicKey"] + payload[
                            "URLwithFactCheck"] + payload["timestamp"]
                        check_signature(pub_key, sig, signed_data)
                        payload["_id"] = payload["URLToCheckHash"] + payload["fingerPrintPublicKey"] + payload[
                            "URLwithFactCheck"]
                        print("inserting to DB: " + str(payload))
                        db_insert_one(fact_coll, payload)
                        send_http_response(self, 200, ok_response("POST", "publishNewFactCheck",
                            "Received data from POST request, new fact check has been stored."))
                        print("New fact check stored to DB.")
                    except Exception as e:
                        print(str(e))
                        # probably invalid signature (or signed with unknown key):
                        send_http_response(self, 400, error_response("POST", "publishNewFactCheck", str(e)))
            else:
                send_http_response(self, 400, error_response("POST", "publishNewFactCheck", "JSON is not wellformed."))


        elif use_case == "deleteFactCheck":
            payload = payload["deleteFactCheck"]
            if (payload_is_correct(payload, EXPECTED_ATTRIBUTES_DELETEFACTCHECK)):
                # Check if this fact check exists:
                fact_check_filter = {"URLToCheckHash": payload["URLToCheckHash"],
                                     "URLwithFactCheck": payload["URLwithFactCheck"]}
                cursor = db_find(fact_coll, fact_check_filter)
                record = next(cursor, None)
                if (record):
                    cursor = db_find(publisher_coll, {"_id": payload["fingerPrintPublicKey"]})
                    publisher = next(cursor, None)
                    if (publisher):
                        signed_msg = payload["publicKey"] + publisher["publisherName"] + payload[
                            "URLToCheckHash"] + "DELETEFLAG"
                        try:
                            check_signature(publisher["publicKey"],
                                            payload["signatureOnPublicKeyPublisherNameURLToCheckHashDELETEFLAG"],
                                            signed_msg)
                            print("Correct signature, deleting fact check...")
                            deleted_fact = fact_coll.find_one_and_delete(fact_check_filter)
                            msg = "Successfully deleted fact check: " + str(json_util.dumps(deleted_fact))
                            print(msg)
                            send_http_response(self, 200, ok_response("POST", "deleteFactCheck", msg))
                        except Exception as e:
                            # Invalid signature:
                            send_http_response(self, 400, error_response("POST", "deleteFactCheck", str(e)))
                    else:
                        # publisher for this fingerprint does not exist in database:
                        msg = "Cannot find publisher for this fingerprint in database, cannot delete fact check."
                        print(msg)
                        send_http_response(self, 400, error_response("POST", "deleteFactCheck", msg))
                else:
                    # Fact check does not exist in DB:
                    msg = "Fact check does not exist: cannot delete."
                    print(msg)
                    send_http_response(self, 400, error_response("POST", "deleteFactCheck", msg))


        elif use_case == "createAccount":
            payload = payload[use_case]
            if payload_is_correct(payload, EXPECTED_ATTRIBUTES_CREATE_ACCOUNT):
                cursor = publisher_coll.find({"_id": payload["fingerPrintPublicKey"]})
                exists_account = next(cursor, None)
                if (exists_account):
                    send_http_response(self, 400, error_response("POST", "createAccount", "There is already a DB Entry for this account"))
                else:
                    try:
                        pub_key = payload["publicKey"]
                        sig = payload["signatureOnPublicKeyPublisherName"]
                        signed_data = payload["publicKey"] + payload["publisherName"]
                        check_signature(pub_key, sig, signed_data)
                        questionable_fingerprint = payload["fingerPrintPublicKey"]
                        check_fingerprint(pub_key, questionable_fingerprint)
                        payload["_id"] = questionable_fingerprint
                        payload.pop("fingerPrintPublicKey")
                        payload["requestCounter"] = 0
                        db_insert_one(publisher_coll, payload)
                        send_http_response(self, 200, ok_response("POST", "createAccount",
                            "Received data from POST request, new account has been stored."))
                        print("New account stored to DB.")
                    except Exception as e:
                        print(str(e))
                        # probably invalid signature:
                        send_http_response(self, 400, error_response("POST", "createAccount", str(e)))
            else:
                send_http_response(self, 400, error_response("POST", "createAccount", "JSON is not wellformed."))


        elif use_case == "deleteAccount":
            payload = payload["deleteAccount"]
            if (payload_is_correct(payload, EXPECTED_ATTRIBUTES_DELETE_ACCOUNT)):
                # Check if this publisher exists:
                publisher_check_filter = {"_id": payload["fingerPrintPublicKey"]}
                cursor = db_find(publisher_coll, publisher_check_filter)
                publisher = next(cursor, None)
                if (publisher):
                    signed_msg = payload["fingerPrintPublicKey"] + publisher["publisherName"] + "DELETEFLAG"
                    print("Signed msg: " + str(signed_msg))
                    try:
                        pub_key = payload["publicKey"]
                        check_signature(pub_key, payload["signatureOnFingerPrintPublicKeyPublisherNameDELETEFLAG"],
                                        signed_msg)
                        print("Correct signature, deleting publisher...")
                        deleted_publisher = publisher_coll.find_one_and_delete(publisher_check_filter)
                        msg = "Successfully deleted publisher: " + str(json_util.dumps(deleted_publisher))
                        print(msg)
                        send_http_response(self, 200, ok_response("POST", "deleteAccount", msg))
                    except Exception as e:
                        # Invalid signature:
                        send_http_response(self, 400, error_response("POST", "deleteAccount", str(e)))
                else:
                    # account does not exist in DB:
                    msg = "publisher does not exist: cannot delete."
                    print(msg)
                    send_http_response(self, 400, error_response("POST", "deleteAccount", msg))
            else:
                send_http_response(self, 400, error_response("POST", "deleteAccount", "JSON is not wellformed."))


        elif use_case == "searchPublisher":
            payload = payload["searchPublisher"]
            if (payload_is_correct(payload, EXPECTED_ATTRIBUTES_SEARCH_PUBLISHER)):
                try:
                    search_term = payload["searchTerm"]
                    timestamp = payload["timestamp"]  # not used for now, could be used for efficiency monitoring later

                    # search by name:
                    cursor = publisher_coll.find({"publisherName": search_term})
                    publishers_by_name_list = collect_entries(cursor)
                    for i in range(len(publishers_by_name_list)):
                        publishers_by_name_list[i] = enrich_publisher_info(publishers_by_name_list[i])
                    # search by fingerprint:
                    cursor = publisher_coll.find({"_id": search_term})
                    publisher_by_fingerprint = next(cursor, None)  # can be at most one
                    if (publisher_by_fingerprint):
                        publisher_by_fingerprint = enrich_publisher_info(publisher_by_fingerprint)

                    # set attributes in response body:
                    body = {}
                    body["searchTerm"] = search_term
                    body["resultsByPublisherNameAmount"] = len(publishers_by_name_list)
                    body["hasResultByFingerPrint"] = True if publisher_by_fingerprint else False
                    body["resultByFingerPrint"] = publisher_by_fingerprint
                    body["resultsByPublisherName"] = publishers_by_name_list
                    body["status"] = "OK"

                    response = {"searchPublishersResult": body}
                    send_http_response(self, 200, json.dumps(response))
                except Exception as e:
                    send_http_response(self, 400, error_response("POST", "searchPublisher", str(e)))

            else:
                send_http_response(self, 400, error_response("POST", "searchPublisher", "JSON is not wellformed."))

        else:
            send_http_response(self, 400, error_response("POST", "unknown", "Unknown use case/Data not readable: %s" % payload_string))

    else: #payload attribute values malformed:
        send_http_response(self, 400, error_response("POST", use_case, df.is_valid_payload(payload) + " are incorrect"))



def process_GET_request(self):
    urlcomps = self.path.split("/")
    if (len(urlcomps) < 3):
        raise Exception("Malformed request. No URLToCheckHash provided?")
    del urlcomps[0]  # first item is always empty
    endpoint = urlcomps[0]  # either "factChecks" or "publishers"
    if (not (endpoint == "factChecks" or endpoint == "publishers")):
        raise Exception("Malformed request. Endpoint for GET requests must be either 'factChecks' or 'publishers'.")
    url_hash = urlcomps[1]  # second item of the url is the URLtoCheckHash

    use_case = "unknown:"
    if endpoint == "factChecks":
        cursor = db_find(fact_coll)
        db_string = ""
        if url_hash == "*":  # only for debugging, GET /factChecks/* sends whole DB
            use_case = '"db":'
            db_string = stringify_DB(cursor, [])
            # send whole db:
            print("Sending entire DB...")
            send_http_response(self, 200, "{" + use_case + db_string + "}")
            return
        elif len(url_hash) > 1:
            try:
                if(len(urlcomps) != 3): raise Exception("Call to endpoint 'factChecks' must contain exactly two parameters <URLToCheckHash> and <fingerPrintPublicKey>.")
                if not df.check_hash(url_hash): raise Exception("URL hash is not a valid SHA 512 hash.")
                finger_print = urlcomps[2]
                #TODO checkFingerprint() broken. Once fixed, uncomment this line:
                # if not df.checkFingerprint(finger_print): raise Exception("Fingerprint is not a valid SHA1 hash")

                use_case = '"specificFactCheck":'
                # increment request counter (fails silently, if not found)
                publisher_coll.find_one_and_update({"_id": finger_print}, {'$inc': {"requestCounter": 1}})

                db_filter = {"URLToCheckHash": url_hash, "fingerPrintPublicKey": finger_print}
                cursor = db_find(fact_coll, db_filter)
                db_string = stringify_DB(cursor, ["signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp",
                                                    "URLwithFactCheck", "publisherName", "timestamp"])
            except Exception as e:
                print(str(e))
                send_http_response(self, 400, error_response("GET", use_case, str(e)))
                return

        if len(db_string) < 3:
            send_http_response(self, 404, error_response("GET", "specificFactCheck", "No DB entry found."))
        else: # send found publishers
            print("Sending specific fact check: " + db_string)
            send_http_response(self, 200, "{" + use_case + db_string + "}")

    elif endpoint == "publishers":
        facts_list = []
        if (len(urlcomps) != 3): raise Exception(
            "Malformed request: URL for the endpoint 'publishers' should consist of three components: Either \n 'publishers/page/<page-number>' or 'publishers/<URLToCheckHash>/*' ")

        if urlcomps[1] == "page":  # schema:  /publishers/page/<page-number>
            use_case = "allPublishers"
            print("use case: " + use_case)
            try:
                if (urlcomps[2] == ""): raise Exception("Request provided no page number.")
                requested_page = int(urlcomps[2])
                print("requested page: " + str(requested_page))
                cursor = publisher_coll.find(filter={}).sort("requestCounter", pymongo.DESCENDING)
                max_publisher_entries = publisher_coll.count_documents({})
                print("publishers in db: " + str(max_publisher_entries))
                available_pages = ceil(max_publisher_entries / MAX_ENTRIES_PER_PAGE)
                print("available pages: " + str(available_pages))
                if (requested_page <= available_pages and requested_page > 0):
                    # skip until requested page:
                    current_page = 1
                    while (current_page < requested_page):
                        for i in range(10): cursor.next()
                        current_page += 1
                    # collect requested entries:
                    publishers_list = collect_entries(cursor, limit=MAX_ENTRIES_PER_PAGE)
                    page_entries = len(publishers_list)
                    for i in range(page_entries):
                        publishers_list[i] = enrich_publisher_info(publishers_list[i])

                    payload = {"status": "OK", "requestedPage": requested_page, "availablePages": available_pages,
                               "pageEntries": page_entries, "publisherList": publishers_list}
                    response = {use_case: payload}
                    send_http_response(self, 200, json_util.dumps(response))

                else:  # requested page does not exist:
                    send_http_response(self, 404,
                        error_response("GET", use_case, "No publishers available on page %s." % requested_page))
            except Exception as e:
                send_http_response(self, 400, error_response("GET", use_case, str(e)))

        elif urlcomps[2] == "*":  # schema:  /publishers/<urlToCheckHash>/*
            use_case = "publishersForSpecificLink"
            if df.check_hash(url_hash):
                cursor = fact_coll.find(filter={"URLToCheckHash": url_hash}, projection=["fingerPrintPublicKey"])
                facts_list = collect_entries(cursor)
                print(facts_list)
                for fact_dict in facts_list:
                    # find publisherName for this fact's fingerPrint in publisher collection:
                    fingerPrint = fact_dict["fingerPrintPublicKey"]
                    publisher_dict = publisher_coll.find_one({"_id": fingerPrint})
                    # add to this fact_dict for response:
                    fact_dict["publicKey"] = publisher_dict["publicKey"]
                    fact_dict["publisherName"] = publisher_dict["publisherName"]
                    fact_dict["signatureOnPublicKeyPublisherName"] = publisher_dict["signatureOnPublicKeyPublisherName"]
                    # _id is contained by default, no matter the projection, remove that:
                    fact_dict.pop("_id")
                # at this point, the facts_list is actually a publisher_list, because
                # we converted each fact dict to a publisher dict above:
                publisher_list = facts_list
                print(publisher_list)

                if len(publisher_list) < 1:
                    send_http_response(self, 404, error_response("GET", "publishersForSpecificLink", "No DB entry found."))
                else:
                    response = {use_case: publisher_list}
                    send_http_response(self, 200, json_util.dumps(response))
            else:
                send_http_response(self, 400, error_response("POST", use_case, "URL is incorrect"))

        else:  # neither '*' as third url component nor 'page' as second url component:
            raise Exception("No such method 'GET /publishers/%s/%s'. Did you mean 'GET /publishers/%s/*' ?" % (
                urlcomps[1], urlcomps[2], urlcomps[1]))



    else:
        send_http_response(self, 404, error_response("GET", "unknown", "Requested resource unknown: %s." % urlcomps[0]))


# End of helper functions

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            process_GET_request(self)
        except Exception as e:
            print(str(e))
            send_http_response(self, 400, error_response("GET", "unknown", str(e)))

    def do_POST(self):
        path = self.path
        content_length = int(self.headers['Content-Length'])
        payload_bytes = self.rfile.read(content_length)
        payload_string = payload_bytes.decode('utf-8')

        if path == POST_END_POINT:
            try:
                process_POST_request(payload_string, self)
            except Exception as e:
                send_http_response(self, 400, error_response("POST", "unknown", str(e)))
                raise e
        elif path == POST_END_POINT + "/deleteDB":

            try:
                fact_coll.delete_many({})
                publisher_coll.delete_many({})
                send_http_response(self, 200, ok_response("POST", "deleteDB", "DB successfully deleted"))
            except Exception as e:
                print(str(e))
                send_http_response(self, 400, error_response("POST", "deleteDB", str(e)))

        else:
            print("Called a wrong POST request: unknown path: %s" % self.path)
            send_http_response(self, 400, error_response("POST", "unknown", "unknown end point: %s" % self.path))


if __name__ == "__main__":

    myServer = HTTPServer((HOST_NAME, HOST_PORT), Handler)
    print(time.asctime(), "Server started on - %s:%s" % (HOST_NAME, HOST_PORT))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server stopped - %s:%s" % (HOST_NAME, HOST_PORT))
