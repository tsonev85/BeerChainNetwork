import hashlib


class CryptoUtils(object):

    @staticmethod
    def calc_sha256(text):
        """
        Returns a hashed string of hexadecimal digits using sha256.
        :param text: <str> Text to hash
        :return: <str>
        """

        hash_object = hashlib.sha256(str(text).encode())
        return hash_object.hexdigest()

    @staticmethod
    def sign_transaction(private_key, data):
        pass
