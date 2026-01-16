import pyotp


def generate_verification_code(digits: int):
    totp = pyotp.TOTP(pyotp.random_base32(), digits=digits)
    return totp.now()
