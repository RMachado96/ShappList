
ACCEPTED_PROVIDERS = ['gmail','hotmail','outlook']

NUMERIC_RANGE = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
UPPER_ALPHA_RANGE = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
LOWER_ALPHA_RANGE = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
DASH_CHAR_CODE = 45
UNDERSCORE_CHAR_CODE = 95
AT_CHAR_CODE = 64
DOT_CHAR_CODE = 46
FULL_CHAR_LIST_EMAIL = [45, 46, 64, 95, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]


def remove_trailing(ver_str):
    return ver_str.replace('\n', '').replace('\r', '')

def create_char_list(ver_str):
    ret_list = []
    for i in ver_str:
        ret_list.append(ord(i))

    return ret_list

def has_at_char(char_list):

    has_char = False

    for i in char_list:
        if(i == AT_CHAR_CODE):
            has_char = True

    return has_char

def has_illegal_chars(char_list):

    is_illegal = False

    for i in char_list:
        if(i not in FULL_CHAR_LIST_EMAIL):
            is_illegal = True

    return is_illegal



def email_has_accepted_provider(email_str):

    at_split = email_str.split('@')
    dot_split = at_split[1].split('.')

    if(dot_split[0] in ACCEPTED_PROVIDERS):
        return True
    else:
        return False

def wrapper(email):

    treated_email = remove_trailing(email)
    emailList = create_char_list(treated_email)

    if(has_at_char(emailList)):
        if(not has_illegal_chars(emailList)):
            if(email_has_accepted_provider(treated_email)):
                return True
            else:
                print("Invalid provider")
                return False
        else:
            print("Invalid character")
            return False
    else:
        print("Invalid email")
        return False


