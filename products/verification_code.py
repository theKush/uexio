import hashlib
import string
# return the verification code created for the product
def verification_code(product):
    return "%s%0.3i" % (letter_code(product.timestamp), product.id)
# use hash value and create letter codes
def letter_code(obj, size=3):
    return md5hash(obj)[:size].translate(string.maketrans('0123456789', 'GHIJKLMNOP')).upper()
# use md5hashes and return a hash value
def md5hash(obj):
    md5 = hashlib.md5()
    md5.update(str(obj))
    return md5.hexdigest()
