"""
CRC functions. Creates checksums for all the message payloads in bytes
"""

from crc import Calculator, Configuration



def compute_crc(payload, nbtyes = 4): 
    """
    I got the CRC and checksum from https://reveng.sourceforge.io/crc-catalogue/all.htm.
    We choose the algorithm **CRC-32/XFER** because 
    1. *The algorithm is evidenced by a widely-available implementation that can calculate CRCs for any desired message.*
    as the webpage ensures us.
    2. It returns exactly 4 bytes (which is the length we desire).

    :param payload: message payload to convert to CRC
    :type payload: bytes
    :param nbytes: number of bytes to compress to in the CRC compression
    :type nbytes: int

    :return:
        CRC (string) -- CRC-32/XFER CRC of 4 bytes

    :formula:
        CRC-32/XFER https://reveng.sourceforge.io/crc-catalogue/all.htm
    """
    prefix = "<compute crc> "
    if type(payload) != bytes:
        print(prefix + "error: message is not in bytes")
        return False
    
    # name="CRC-32/XFER" <- type of checksum configuration
    config = Configuration(
        width=32, polynomial=0x000000af, 
        init_value=0x00000000, reverse_input=False, 
        reverse_output=False, final_xor_value=0x00000000
        )

    calculator = Calculator(config)
    crc = calculator.checksum(payload)

    print(prefix + "resulting CRC: " + str(crc))

    return crc




def old_compute_crc(payload, nbytes=4): 
    """
    compute the crc of the message, using the ammount of bytes permitted

    :param payload: message payload to convert to CRC
    :type payload: bytes
    :param nbytes: number of bytes to compress to in the CRC compression
    :type nbytes: int

    :return:
        CRC (string) -- custom CRC after adding the byte values plus the bytearray to int

    :formula:
        n = nbytes
        CRC = [ sum_byte_by_byte(payload) + concat_numbers_left_to_right(payload) + concat_numbers_right_to_left(payload) ] % 256^n
        description: second page of https://jamboard.google.com/d/1ERZewSRK3-BmkMuzH5g7swd7OwKDTgcD2FevFguLn2g/edit?usp=sharing
    """
    prefix = "<compute crc> "
    if type(payload) != bytes:
        print(prefix + "error: message is not in bytes")
        return False

    divisor = pow(256, nbytes)-1 #: if the divisor is a multiple of 256, no changes are appreciated after a small change

    sum = 0
    left = ""
    right = ""
    for i in range(len(payload)):
        byte = payload[i:(i+1)]
        num = int.from_bytes(byte, "little")
        sum = sum + num
        if num != 0:
            left = left + str(num)
            right = str(num) + right
    sum = sum + int(left) + int(right)
    crc = sum % divisor
    print(prefix + " message int: " + str(sum) + ", divisor: " + str(divisor))
    print(prefix + "resulting CRC: " + str(crc))

    return crc