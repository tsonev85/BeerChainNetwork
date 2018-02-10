import hashlib
import base58


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
    def byte_to_hex(pub_key_sha):
        result = ""
        for n in pub_key_sha:
            result += ''.join(format(n, '02X'))
        return result

    @staticmethod
    def hex_to_byte(hex_string):
        if len(hex_string) % 2 != 0:
            raise Exception('Invalid HEX')
        return bytes.fromhex(hex_string)

    @staticmethod
    def sha_256(pub_key_sha):
        hash_object = hashlib.sha256(pub_key_sha)
        return bytearray(hash_object.digest())

    @staticmethod
    def ripe_md_160(pub_key_sha):
        hash_obect = hashlib.new('ripemd160', pub_key_sha)
        return bytearray(hash_obect.digest())

    @staticmethod
    def append_bitcoin_network(ripe_hash, network):
        extended = bytearray(len(ripe_hash) + 1)
        extended[0] = network
        extended[1:] = ripe_hash
        return extended

    @staticmethod
    def concat_address(ripe_hash, checksum):
        ret = bytearray(len(ripe_hash) + 4)
        ret = ripe_hash[:]
        ret[-4:] = checksum[:4]
        return ret

    @staticmethod
    def base_58_encode(array):
        return base58.b58encode(bytes(array))
