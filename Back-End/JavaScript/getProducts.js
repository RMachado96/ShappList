var currentSelectedCat = '';
var currentSelectedSubCat = '';

function changeCurrentSelectedCat(newCat){

    currentSelectedCat = newCat;
    return true;
}

function changeCurrentSelectedSubCat(newSubCat){

    currentSelectedSubCat = newSubCat;
    return true;
}

function catMenuChange(newValue, catType){ //to be executed onclick
    if(document.getElementById("search").value != ""){
        document.getElementById("search").value = "";
    }

    if(catType == 'subCat'){
        changeCurrentSelectedSubCat(newValue);
        //changeCurrentSelectedCat('');
        sidebar();
    }
    else if(catType == 'cat'){
        changeCurrentSelectedCat(newValue);
        changeCurrentSelectedSubCat('');
        sidebar();
    }
    getProductInfo('itemPrice','ASC');
}

function getDiscountedProducts(){
    console.log('Creating request');
    var ajaxRequest = new XMLHttpRequest();

    ajaxRequest.onreadystatechange = function() {
        if (ajaxRequest.readyState == 4) {   // XMLHttpRequest.DONE == 4
            if (ajaxRequest.status == 200) {


                var responseData = JSON.parse(ajaxRequest.responseText);

                sidebar();
                changeElements(responseData);

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
    ajaxRequest.open("POST", "https://shapplist.pythonanywhere.com/api/productServices/api_getProductsWithDiscount", true);
    ajaxRequest.setRequestHeader("content-type", "application/json; charset=utf-8");
    ajaxRequest.send();
}

function getProductInfo(orderBy,clause){

        var sbKeyValue = document.getElementById("search").value;
        console.log(orderBy);
        console.log(clause);

        //var itemCatValue = document.getElementById(itemCatValue).value;

        //var itemSubCatValue = document.getElementById(itemSubCatValue).value;
        var itemCatValue = currentSelectedCat;

        var itemSubCatValue = currentSelectedSubCat;

        var data = JSON.stringify({'searchbar_keyword' : sbKeyValue, 'category' : itemCatValue, 'sub_category' : itemSubCatValue,'orderBy' : orderBy, 'clause' : clause});

        //var data = JSON.stringify({'searchbar_keyword' : sbKeyValue, 'category' : '', 'sub_category' : ''});

        //var data = JSON.stringify({'searchbar_keyword' : sbKeyValue});
        var endPoint = "https://shapplist.pythonanywhere.com/api/productServices/api_getProducts";

        if(sbKeyValue || itemCatValue || itemSubCatValue){
            var responseData = sendProductRequest(data,endPoint);
        }
        else{
            var responseData = sendProductRequest(data,endPoint);
        }

    //do something to show that you should write something
}

function sendProductRequest(data,endPoint){
    console.log('Creating request');
    var ajaxRequest = new XMLHttpRequest();

    ajaxRequest.onreadystatechange = function() {
        if (ajaxRequest.readyState == 4) {   // XMLHttpRequest.DONE == 4
            if (ajaxRequest.status == 200) {


                var responseData = JSON.parse(ajaxRequest.responseText);

                changeElements(responseData);

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

function changeElements(responseData){
    var totalContainers = responseData['totalSize'];
    var finalHTML = '';



    for(i = 0; i < totalContainers; i++){
        var minPrice = 9999;
        var maxPrice = 0;
        var tempPrice = 0;
        var isDiscounted = false;
        var discountHTMLImage = "";
        var discountArr = responseData['products']['prod' + i.toString()]['desconto']
        var discountedStores = [];

        for(j = 0; j < responseData['products']['prod' + i.toString()]['preco'].length; j++ ){
           tempPrice = responseData['products']['prod' + i.toString()]['preco'][j];

           if(maxPrice < tempPrice){
               maxPrice = tempPrice
           }
           if(minPrice > tempPrice){
               minPrice = tempPrice
           }

        }

        for(k = 0; k <discountArr.length; k++){
            if(discountArr[k] != 1){
                isDiscounted = true;
                discountedStores.push(responseData['products']['prod'+i.toString()]['storeID'][k]);
                discountHTMLImage = `<img class="over-image" src="static/ShappList/resources/products/discount.png">`;
            }
        }

        var margin = '.75rem;';
        if(i%2 == 0){
           margin = '-' + margin;
        }
        //onclick ="showOverlayIndProdDivFluid([`+responseData['products']['prod'+i.toString()]['id']+`],[`+responseData['products']['prod'+i.toString()]['storeID']+`],'`+responseData['products']['prod'+i.toString()]['path']+`','`+responseData['products']['prod'+i.toString()]['nome']+`',[`+ responseData['products']['prod' + i.toString()]['preco']+`])"
        var tempHTML = `<div class="col-6 col-md-3 col-sm-4 col-xl-2 div-fluid" >
        <div>
          <div class="images text-center">
            <img class="img-fluid" src="/static/ShappList/resources/products`+ responseData['products']['prod' + i.toString()]['path'] +  `">
            `+discountHTMLImage+`
            <button type="button" class="btnAdd btn" name="button" onclick="quickAddProduct([`+responseData['products']['prod'+i.toString()]['id']+`])">+</button>
          </div>` +
          //`<div class="name">` + responseData['products']['prod' + i.toString()]['nome'] + ` and ` + responseData['products']['prod' + i.toString()]['marca']+`</div>` +
         `<div class ="groupNameBrand">` +
          ` <div class="name">` + responseData['products']['prod' + i.toString()]['nome'] + `</div>` +
          ` <div class="brand">` + responseData['products']['prod' + i.toString()]['marca'] + `</div>` +
         `</div>` +
          `<div class="price">
            <b>` + minPrice.toString() + " - " + maxPrice.toString()+ "€ " + responseData['products']['prod' + i.toString()]['tipo_preco'] +` </b>
          </div>
          <div class="details text-center">
            <a onclick="showOverlayIndProdDivFluid([`+responseData['products']['prod'+i.toString()]['id']+`],[`+responseData['products']['prod'+i.toString()]['storeID']+`],'`+responseData['products']['prod'+i.toString()]['path']+`','`+responseData['products']['prod'+i.toString()]['nome']+`',[`+ responseData['products']['prod' + i.toString()]['preco']+`],`+isDiscounted+`,[`+discountedStores+`])">Detalhes</a>
          </div>
            </div>
        </div>`;
        finalHTML = finalHTML + '\n' + tempHTML;
    }

    document.getElementById("mainContainer").innerHTML = finalHTML;
}