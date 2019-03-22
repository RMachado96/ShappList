##  Hashing event should be triple SHA256
##  Once a new user registers, a random salt is generated for him and stored on the DB
##  This salt will be associated with the username/email
##  Salt will be applied to all hashing algo passes
##  Login event will take username, get salt, hash password with salt, compare back to DB
## and answear back based on that
##  Storage consists on the encoding using Base64 of the hex digest output
##  Salt should be a random number between 0 - 9999
##
##
##  Tokens are created by joining the current Unix time, the username and a random int
## between 0 and 9999 and hashing them using SHA512
##  Maybe generate different token styles:
##   randint-user-unix-randint
##   randint-randint-user-unix
##   user-randint-unix-randint
##   unix-randint-user-randint
##   user-unix-randint-randint
##   unix-randint-randint-user




import hashlib
import base64
import time
from random import randint


def full_hash(password, salt):

    final_hash = hf_sha256(hf_sha256(hf_sha256(password, salt), salt), salt)

    print('Final hash: ' + final_hash)




def hf_sha256(password, salt):
    
    salted_password = password + salt

    print(salted_password)

    #salted_password_b64 = base64.standard_b64encode(str.encode(salted_password))
    #print(salted_password_b64)

    hasher = hashlib.sha256()

    hasher.update(str.encode(salted_password))

    hashed_password = hasher.hexdigest()

    print(hashed_password)

    return(hashed_password)


def gen_token(username):

    token_dict = {}

    curr_time = curr_unix()

    token = hf_sha512(username, curr_time)
    token_dict['token'] = token
    token_dict['gen_time'] = curr_time

    print(token_dict)

    return(token_dict)


def rand_int(min, max):
    new_rand = randint(min, max)
    print(new_rand)
    return(new_rand)


def curr_unix():
    return int(time.time())

def hf_sha512(username, curr_time):
    full_text = username + str(curr_time) + str(rand_int(0, 9999))
    print(full_text)

    hasher = hashlib.sha3_512()

    hasher.update(str.encode(full_text))
    token = hasher.hexdigest()
    print(token)
    return(token)


#sha256_hash_func('test', 'salt')
full_hash('test', 'salt')

gen_token('dymsi')