function signUp(){
    var localStorageToken = 'ShappListToken';
    var idValue = document.getElementById("username").value;
    var pwValue = document.getElementById("password").value;
    var emailValue = document.getElementById("email").value;
    var phoneValue = document.getElementById("phoneNumber").value;

    if(check_email(emailValue)  && checkNumber(phoneValue)){
        var emailValueNoTrailing = remove_trailing(emailValue);
        var finalEmail = remove_spaces(emailValueNoTrailing);

        var data = JSON.stringify({"username" : idValue, "password" : pwValue,"email" : finalEmail, "phoneNum" : phoneValue});
        var endPoint = "https://shapplist.pythonanywhere.com/api/authServices/api_signup";

        if(document.cookie){
            document.cookie = 'token=';
        }

        var responseData = signUpSendRequest(data,endPoint);
    }
    else{
      document.getElementById("errorMsg").style.display = "block";
	  document.getElementById("email").style.borderColor ="red";
	  document.getElementById("phoneNumber").style.borderColor ="red";
	  document.getElementById("errorMsg").innerHTML = "Por favor introduza um número de telefone e email válidos.";
    }


}
function logOut(){

    //document.cookie = 'token=';
    document.cookie = 'token=;path=/';
    window.location.replace("/login");

}

function signIn(){

    var emailValue = document.getElementById("email").value;
    var pwValue = document.getElementById("password").value;
    if(check_email(emailValue)){

        var emailValueNoTrailing = remove_trailing(emailValue);
        var finalEmail = remove_spaces(emailValueNoTrailing);

        var data = JSON.stringify({"email" : finalEmail, "password" : pwValue});
        var endPoint = "https://shapplist.pythonanywhere.com/api/authServices/api_login";

        var responseData = signInSendRequest(data,endPoint);
    }

     else{
         document.getElementById("errorMsg").style.display = "block";
	     document.getElementById("email").style.borderColor ="red";
	     document.getElementById("errorMsg").innerHTML = "Por favor introduza um email válido.";
    }

}


function signUpSendRequest(data,endPoint){
    console.log('Creating request');
    var ajaxRequest = new XMLHttpRequest();

    ajaxRequest.onreadystatechange = function() {
        var localStorageToken = 'ShappListToken';
        if (ajaxRequest.readyState == 4) {   // XMLHttpRequest.DONE == 4
            if (ajaxRequest.status == 200) {




                var responseData = JSON.parse(ajaxRequest.responseText);

                if(responseData.status == 300){

                    document.getElementById("errorMsg").style.display = "block";
            	    document.getElementById("email").style.borderColor ="red";
            	    document.getElementById("phoneNumber").style.borderColor ="red";
            	    document.getElementById("errorMsg").innerHTML = "Email ou número de telefone já existe!";
                }
                else{
                    var message = responseData['message'];
                    var token = responseData['token'];


                    document.cookie = 'token = ' + token + ';path=/';

                    window.location.replace("/products");
                }

            }
            else if (ajaxRequest.status == 400) {
                console.log("Server error 400");
            }
            else {
                console.log("Server error 400");
            }
        }
    };

    console.log('Sending request');
    ajaxRequest.open("POST", endPoint, true);
    ajaxRequest.setRequestHeader("content-type", "application/json; charset=utf-8");

    ajaxRequest.send(data);

}

function signInSendRequest(data,endPoint){
    console.log('Creating request');
    var ajaxRequest = new XMLHttpRequest();

    ajaxRequest.onreadystatechange = function() {
        var localStorageToken = 'ShappListToken';
        if (ajaxRequest.readyState == 4) {   // XMLHttpRequest.DONE == 4
            if (ajaxRequest.status == 200) {


                var responseData = JSON.parse(ajaxRequest.responseText);

                if(responseData.status == 400){

                    document.getElementById("errorMsg").style.display = "block";
            	    document.getElementById("email").style.borderColor ="red";
            	    document.getElementById("password").style.borderColor ="red";
            	    document.getElementById("errorMsg").innerHTML = "Email ou password incorrecto(s).";
                }
                else{

                    var message = responseData['message'];
                    var token = responseData['token'];
                    var flag = responseData['updatedDefaultList'];
                    console.log(responseData['defaultList']);
                    console.log(flag);


                    document.cookie = 'token = ' + token + ';path=/';

                    if(flag){
                        localStorage.setItem("activeList",responseData['defaultList'].toString());
                    }
                    else{
                        localStorage.setItem("activeList","0");
                    }

                    window.location.replace("/products");
                }

            }
            else if (ajaxRequest.status == 400) {
                console.log("Server error");

            }
            else {
                console.log("Server error 400");
            }
        }
    };

    console.log('Sending request');
    ajaxRequest.open("POST", endPoint, true);
    ajaxRequest.setRequestHeader("content-type", "application/json; charset=utf-8");

    ajaxRequest.send(data);

}