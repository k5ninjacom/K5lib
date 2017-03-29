import string

# https://docs.python.org/3/library/secrets.html
# create a alphanumeric password with at least one lowercase character, at least one uppercase character, and at least three digits
# Returns String
def gen_passwd(length):
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
            break
    return password


