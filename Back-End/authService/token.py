import hashlib
import base64
import time
from random import randint


def number_list_generator(min, max):

    ret_list = []

    for i in range(min, max + 1):
        ret_list.append(i)

    #print(ret_list)

    return ret_list

def ascii_to_char_list_generator(ascii_list):
    ret_list = []

    for i in ascii_list:
        ret_list.append(chr(i))

    return ret_list

def rand_numb(min_prov, max_prov):

    rand_int = randint(min_prov, max_prov)

    return rand_int

def rand_string(size, char_list):

    list_len = len(char_list)

    ret_str = ''

    for i in range(size):
        ret_str += char_list[rand_numb(0, list_len - 1)]

    return ret_str

def curr_unix():
    return int(time.time())


def hf_sha512(unhashed_str):
    hasher = hashlib.sha3_512()

    hasher.update(str.encode(unhashed_str))
    token = hasher.hexdigest()
    #print(token)
    return(token)


def token_style_gen(username):
    FINAL_FULL_ALPHA_NUMERIC_CHAR_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    rand_padding_1 = rand_string(8, FINAL_FULL_ALPHA_NUMERIC_CHAR_LIST)
    rand_padding_2 = rand_string(8, FINAL_FULL_ALPHA_NUMERIC_CHAR_LIST)
    unix_str = str(curr_unix())
    style_int = rand_numb(1, 6)

    #print(rand_padding_1)
    #print(rand_padding_2)
    #print(unix_str)
    #print(username)

    if(style_int == 1):
        final_str = rand_padding_1 + username + unix_str + rand_padding_2

    elif(style_int == 2):
        final_str = rand_padding_1 + rand_padding_2 + username + unix_str

    elif(style_int == 3):
        final_str = username + rand_padding_2 + unix_str + rand_padding_1

    elif(style_int == 4):
        final_str = username + unix_str + rand_padding_2 + rand_padding_1

    elif(style_int == 5):
        final_str = unix_str + rand_padding_2 + username + rand_padding_1

    else:
        final_str = unix_str + rand_padding_2 + rand_padding_1 + username
    
    #print(final_str)

    token = hf_sha512(final_str)

    print(token)
    
    return token



    


NUMERIC_ASCII_LIST = number_list_generator(48, 57)
LOWER_ALPHA_ASCII_LIST = number_list_generator(97, 122)
UPPER_ALPHA_ASCII_LIST = number_list_generator(65, 90)
COMPLETE_CHAR_ASCII_LIST_LOWER = number_list_generator(33, 47)
COMPLETE_CHAR_ASCII_LIST_UPPER = number_list_generator(48, 57)
COMPLETE_CHAR_ASCII_LIST_OUTLIERS = number_list_generator(58, 64)
COMPLETE_CHAR_ASCII_LIST_TOTAL = number_list_generator(91, 96)
FULL_ALPHA_ASCII_LIST = LOWER_ALPHA_ASCII_LIST + UPPER_ALPHA_ASCII_LIST
FULL_ALPHA_NUMERIC_ASCII_LIST = NUMERIC_ASCII_LIST + FULL_ALPHA_ASCII_LIST


#print(NUMERIC_ASCII_LIST)
#print(LOWER_ALPHA_ASCII_LIST)
#print(UPPER_ALPHA_ASCII_LIST)
#print(COMPLETE_CHAR_ASCII_LIST_LOWER)
#print(COMPLETE_CHAR_ASCII_LIST_UPPER)
#print(COMPLETE_CHAR_ASCII_LIST_OUTLIERS)
#print(COMPLETE_CHAR_ASCII_LIST_TOTAL)
#print(FULL_ALPHA_ASCII_LIST)
#print(FULL_ALPHA_NUMERIC_ASCII_LIST)


FULL_ALPHA_NUMERIC_CHAR_LIST = ascii_to_char_list_generator(FULL_ALPHA_NUMERIC_ASCII_LIST)

#print(FULL_ALPHA_NUMERIC_CHAR_LIST)

#print(rand_string(8, FULL_ALPHA_NUMERIC_CHAR_LIST))

print(token_style_gen('dymsi'))

