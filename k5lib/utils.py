import random
import string

def gen_passwd(length):
    if not hasattr(gen_random_string, "rng"):
        gen_random_string.rng = random.SystemRandom() # Create a static variable
        
    return ''.join([ gen_random_string.rng.choice(char_set) for _ in xrange(length) ])

password_charset = string.ascii_letters + string.digits
gen_random_string(password_charset, 32)

