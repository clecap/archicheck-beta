# Author: Mostafa, Abdulrahman

import re


def check_hash(value: str) -> bool:
    """
    Checks, if provided value is a valid SHA-512 hash.
    Parameters:
    value (```str```): string to validate
    Returns:
    ```bool```: True, if value is a valid SHA-512 hash, otherwise false
    """
    match = None
    try:
        # match exactly 128 hexadecimal symbols:
        match = re.match(r'^[A-Fa-f0-9]{128}$', value).group(0)
    except Exception as e:
        pass
    return match is not None

def check_public_key(public_key):
    """
       Checks, if provided value is a valid RSA 4096 Public Key.
    """
    pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$", 0)
    if len(public_key) == 736:
        if re.match(pattern, public_key):
            return re.match(pattern, public_key).span() == (0, 736)
    return False

def check_url(url):
    pattern = re.compile(
        "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",
        0)
    if len(url) <= 2048:
        if re.match(pattern, url):
            return re.match(pattern, url).span() == (0, len(url))
    return False

def check_fingerprint(fingerprint):
    pattern = re.compile("^([0-9]|[a-f]){40}$", 0)
    if re.match(pattern, fingerprint):
        return re.match(pattern, fingerprint).span() == (0, 40)
    return False

def check_time_stamp(time_stamp):
    """
        Checks, if provided value is a valid ISO 8601 timestamp.
    """
    pattern = re.compile(
        "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$",0)
    if re.match(pattern, time_stamp):
        return re.match(pattern, time_stamp).span() == (0, len(time_stamp))
    return False

def is_valid_payload(payload):
    response = ""
    if get_key_if_exists(payload,"URLwithFactCheck")!="":
        if not check_url(get_key_if_exists(payload,"URLwithFactCheck")):
            response += "URLwithFactCheck"
    if get_key_if_exists(payload,"URLTocheck_hash")!="":
        if not check_hash(get_key_if_exists(payload,"URLTocheck_hash")):
            if response != "":
                response += " and URLTocheck_hash"
            else:
                response += "URLTocheck_hash"
    if get_key_if_exists(payload,"fingerPrintPublicKey")!="":
        if not check_fingerprint(get_key_if_exists(payload,"fingerPrintPublicKey")):
            if response != "":
                response += " and fingerPrintPublicKey"
            else:
                response += "fingerPrintPublicKey"
    if get_key_if_exists(payload,"timestamp")!="":
        if not check_time_stamp(get_key_if_exists(payload,"timestamp")):
            if response != "":
                response += " and timestamp"
            else:
                response += "timestamp"
    if get_key_if_exists(payload,"publicKey")!="":
        if not check_public_key(get_key_if_exists(payload,"publicKey")):
            if response != "":
                response += " and publicKey"
            else:
                response += "publicKey"
    return response


def get_key_if_exists(dict, key):
    '''
    Check if *keys (nested) exists in `element` (dict) and if so returns its value.
    '''
    if key in dict:
        return dict[key]
    else:
        for element in dict.values():
            if type(element) == type(dict):
                return get_key_if_exists(element, key)
    return ""
