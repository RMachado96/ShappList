var ACCEPTED_PROVIDERS = ['gmail', 'hotmail', 'outlook','yahoo','msn','live','aol','netcabo'];
var ACCEPTED_DOMAINS = ['com','pt','uk','br','co','net'];
var NUMERIC_RANGE = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57];
var UPPER_ALPHA_RANGE = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90];
var LOWER_ALPHA_RANGE = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122];
var DASH_CHAR_CODE = 45;
var UNDERSCORE_CHAR_CODE = 95;
var AT_CHAR_CODE = 64;
var FULL_CHAR_LIST_EMAIL = [45, 46, 64, 95, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122];

function create_char_list(ver_str) {

    ret_list = [];
    for (i = 0; i < ver_str.length; i++) {
        ret_list.push(ver_str.charCodeAt(i));
    }

    return ret_list;
}

function has_illegal_chars(char_list) {

    for (i = 0; i < char_list.length; i++) {
        if (!(FULL_CHAR_LIST_EMAIL.includes(char_list[i]))) {
            console.log(char_list[i]);
            return true;
        }
    }

    return false;
}

function has_at_char(char_list) {

    for (i = 0; i < char_list.length; i++) {
        if (char_list[i] == AT_CHAR_CODE) {
            return true;
        }
    }
    return false;

}

function email_has_accepted_provider(email_str) {
        at_split = email_str.split('@')
        dot_split = at_split[1].split('.')

        if (ACCEPTED_PROVIDERS.includes(dot_split[0])) {
            return true;
        }
        else {
            return false;
        }

}

function has_domain(ver_str){
    at_split = ver_str.split('@')
    dot_split = at_split[1].split('.')

    if(!(dot_split[1])){
        return false;
    }
    else{
        if(ACCEPTED_DOMAINS.includes(dot_split[1])){
            return true;
        }
        else{
            return false;
        }
    }

}

function remove_trailing(ver_str) {
    return_str = ver_str.replace('\n', '').replace('\r', '');

    return return_str;
}

function remove_spaces(ver_str) {
    return_str = ver_str.replace(' ', '');

    return return_str;
}

function check_email(ver_str) {

    ver_str = remove_trailing(ver_str);
    ver_str = remove_spaces(ver_str);
    char_list = create_char_list(ver_str);


    if(!(has_at_char(char_list))){
        return false;
    }
    if(!(email_has_accepted_provider(ver_str))){
        return false;
    }

    if(!(has_domain(ver_str))){
        return false;
    }

    else{
        if(has_illegal_chars(char_list)){
            return false;
        }
        else{
            return true;
        }
    }
}