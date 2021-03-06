# -*- coding: utf-8 -*-
"""
    Yubikey Python API

    :copyright: © 2011 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import urllib
import string
import Queue
from threading import Thread
from random import sample
import hmac, hashlib
from base64 import b64encode, b64decode


class YubicoClient(object):
    """A client to validate OTP generated by Yubico Yubikeys.

    If you have your own servers against which you want to do the verification
    the replace the :attr:api_urls Example:

        client = YubicoClient(client_id, key)
        client.api_urls = ['custom url 1', 'custom url 2']
    """

    api_urls = [
        'http://api.yubico.com/wsapi/2.0/verify',
        'http://api2.yubico.com/wsapi/2.0/verify',
        'http://api3.yubico.com/wsapi/2.0/verify',
        'http://api4.yubico.com/wsapi/2.0/verify',
        'http://api5.yubico.com/wsapi/2.0/verify',
    ]

    #: Stores the last status response that was received
    last_status = None

    def __init__(self, client_id, key):
        self.client_id = client_id
        self.key = b64decode(key)

    def verify(self, otp, timeout=5):
        """Verfies the OTP by simultaneously calling all servers and returning 
        the first valid response if any.
        """
        query = {
            'id': self.client_id,
            'nonce': ''.join(sample(string.letters, 20)),
            'otp': otp
            }
        query['h'] = self.generate_signature(query)
        url_encoded_query = urllib.urlencode(query)

        # The queue to which all responses are put
        threads = []
        response_queue = Queue.Queue(maxsize=len(self.api_urls))
        for url in self.api_urls:
            thread = Thread(
                target=_call_yubico, 
                args=(url, url_encoded_query, response_queue)
                )
            thread.start()
            threads.append(thread)

        # wait for all the threads with the timeout
        [thread.join(timeout) for thread in threads]

        status = "OTP validation failed"
        while not response_queue.empty():
            response = self.response_to_dict(response_queue.get())
            status = response.get('status')
            if status != 'OK':
                continue

            assert query['otp'] == response['otp'], \
                "Invalid OTP. Cut'n'Paste attack suspected."
            assert query['nonce'] == response.get('nonce'), \
                'Unique nonce does not match'
            assert self.verify_signature(response), \
                'Signature validation failed.'

            # All checks are complete, its a valid OTP
            return True
        else:
            raise Exception(status)

    def generate_signature(self, key_value_pairs):
        """The Yubico Validation Protocol Version 2.0 uses HMAC-SHA-1 
        signatures where the HMAC key to use is the client API key. The steps 
        to generate such a key is below and this method implements steps 1-4
        returning the value of h that could be used for step 5 elsewhere:

          1. Alphabetically sort the set of key/value pairs by key order.
          2. Construct a single line with each ordered key/value pair 
             concatenated using '&', and each key and value contatenated with 
             '='. Do not add any linebreaks. Do not add whitespace. 
             For example: a=2&b=1&c=3.
          3. Apply the HMAC-SHA-1 algorithm on the line as an octet string 
             using the API key as key.
          4. Base 64 encode the resulting value according to RFC 4648, for 
             example, t2ZMtKeValdA+H0jVpj3LIichn4=.
          5. Append the value under key 'h' to the message. 

        `Read More here 
        <http://code.google.com/p/yubikey-val-server-php/wiki/ValidationProtocolV20>`_

        :param key_value_pais: A `dict` of key value pairs that will be used in
            the computation of 'h'
        :return: Base 64 encoded signature
        """
        # Step 1
        keys = key_value_pairs.keys()
        keys.sort()

        # Step 2
        query = '&'.join(
            ['%s=%s' % (k, key_value_pairs[k]) for k in keys if k != 'h']
            )

        # Step 3
        digest = hmac.new(self.key, query, hashlib.sha1).digest()

        # Step 4
        return b64encode(digest)

    def verify_signature(self, result):
        """To verify a signature in a response sent by yubico, the same 
        procedure used in :method:generate_signature is followed on the 
        received key value pairs (excluding h) and the resulting key is checked
        for equality with the sent h

        `Read More here 
        <http://code.google.com/p/yubikey-val-server-php/wiki/ValidationProtocolV20>`_

        :param result: A `dict` with key value pairs sent in the response
        :return: True if verified, else False
        """
        result_copy = result.copy()
        response_signature = result_copy.pop('h')
        constructed_signature = self.generate_signature(result_copy)
        return response_signature == constructed_signature

    def response_to_dict(self, response):
        """The response from the yubico server is a text/plain response with 
        the key and value separated by '=' on different lines

        :param response: the response string as sent by yubico
        """
        result_dict = {}
        for line in response.split('\r\n'):
            if not line: continue
            key, value = line.split('=', 1)
            result_dict[key] = value
        return result_dict


def get_identity_from_otp(otp):
    """YubiKey OTP contains as the initial part, an identity of the YubiKey, 
    and it can be used to identify the user. The identity part is the same 
    for every OTP, and it is the initial 2-16 modhex characters of the OTP. 
    (The identity can be programmed to 0 characters, but then obviously this 
    scheme does not apply.) Since the rest of the OTP is always 32 characters, 
    the method to extract the identity is to remove 32 characters from the end 
    and then use the remaining string, which should be 2-16 characters, as 
    the YubiKey identity.
    """
    return otp[:-32]


def _call_yubico(api_url, query, response_queue):
    """Call the api_url with the query and return the response. This function
    as its name indicates is not intended to be called directly but by the
    threaded part of verify in the main class.

    This is made a function outside the main class to avoid any shared state
    at all.
    """
    url = '%s?%s' % (api_url, query)
    response_queue.put(urllib.urlopen(url).read())
