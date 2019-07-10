//Function to iterate through list

// PingoDoce = 1
// Continente = 2
// Jumbo = 3

var prefix = 'item';

pingoDoce_id = 1;
continente_id = 2;
jumbo_id = 3;

var fullItemDict = {}

userPrefs = [1, 2, 3]; //-> lista de stores definidas pelo user

pingoDoce_item_id = [];
pingoDoce_item_price = []
pingoDoce_item_id_missing = []
pingoDoce_item_name_missing = []
pingoDoce_total_price = 0;
pingoDoce_total_price_string = "";

continente_item_id = []
continente_item_price = []
continente_item_id_missing = []
continente_item_name_missing = []
continente_total_price = 0;
continente_total_price_string = "";

jumbo_item_id = []
jumbo_item_price = []
jumbo_item_id_missing = []
jumbo_item_name_missing = []
jumbo_total_price = 0;
jumbo_total_price_string = "";

function changeUserPrefs(listStores){
    userPrefs = listStores;
    if(userPrefs.length <= 0){
        document.getElementById("supermercado").innerHTML = "Não está a permitir nenhum supermercado!";
        document.getElementById("bestValue").innerHTML ="";
    }
    if(!userPrefs.includes(1)){
        pingoDoce_total_price = 9999;
    }
    if(!userPrefs.includes(2)){
        continente_total_price = 9999;
    }
    if(!userPrefs.includes(3)){
        jumbo_total_price = 9999;
    }


}

function resetEnv(){
    pingoDoce_item_id = [];
    pingoDoce_item_price = []
    pingoDoce_item_id_missing = []
    pingoDoce_item_name_missing = []
    pingoDoce_total_price = 0;
    pingoDoce_total_price_string = "";

    continente_item_id = []
    continente_item_price = []
    continente_item_id_missing = []
    continente_item_name_missing = []
    continente_total_price = 0;
    continente_total_price_string = "";

    jumbo_item_id = []
    jumbo_item_price = []
    jumbo_item_id_missing = []
    jumbo_item_name_missing = []
    jumbo_total_price = 0;
    jumbo_total_price_string = "";
    fullItemDict = {}
}

function setupItemArrays(){



    for(j = 0; j < fullItemDict['totalItems']; j++){


        if(fullItemDict[prefix + j.toString()]['storeArray'].includes(pingoDoce_id)){
            pingoDoce_item_id.push(fullItemDict[prefix + j.toString()]['itemID']);
            pingoDoce_item_price.push(fullItemDict[prefix + j.toString()]['priceArray'][fullItemDict[prefix + j.toString()]['storeArray'].indexOf(pingoDoce_id)] * fullItemDict[prefix + j.toString()]['itemQuantity']);
        }
        else{
            pingoDoce_item_id_missing.push(fullItemDict[prefix + j.toString()]['itemID']);
            pingoDoce_item_name_missing.push(fullItemDict[prefix + j.toString()]['itemName']);
            //Maybe also create array to account for the total value of missing items
        }

        if(fullItemDict[prefix + j.toString()]['storeArray'].includes(continente_id)){
            continente_item_id.push(fullItemDict[prefix + j.toString()]['itemID']);
            continente_item_price.push(fullItemDict[prefix + j.toString()]['priceArray'][fullItemDict[prefix + j.toString()]['storeArray'].indexOf(continente_id)] * fullItemDict[prefix + j.toString()]['itemQuantity']);
        }
        else{
            continente_item_id_missing.push(fullItemDict[prefix + j.toString()]['itemID']);
            continente_item_name_missing.push(fullItemDict[prefix + j.toString()]['itemName']);
            //Maybe also create array to account for the total value of missing items
        }

        if(fullItemDict[prefix + j.toString()]['storeArray'].includes(jumbo_id)){
            jumbo_item_id.push(fullItemDict[prefix + j.toString()]['itemID']);
            jumbo_item_price.push(fullItemDict[prefix + j.toString()]['priceArray'][fullItemDict[prefix + j.toString()]['storeArray'].indexOf(jumbo_id)] * fullItemDict[prefix + j.toString()]['itemQuantity']);
        }
        else{
            jumbo_item_id_missing.push(fullItemDict[prefix + j.toString()]['itemID']);
            jumbo_item_name_missing.push(fullItemDict[prefix + j.toString()]['itemName']);
            //Maybe also create array to account for the total value of missing items
        }
    }
}


function getBestPrice(){
    if(pingoDoce_total_price < continente_total_price && pingoDoce_total_price < jumbo_total_price && userPrefs.includes(pingoDoce_id)){
        document.getElementById("supermercado").innerHTML = "O melhor supermercado para si é o Pingo Doce";
        document.getElementById("bestValue").innerHTML = " com um valor total de " + pingoDoce_total_price_string+ "!";
    }
    if(continente_total_price < pingoDoce_total_price && continente_total_price < jumbo_total_price && userPrefs.includes(continente_id)){
        document.getElementById("supermercado").innerHTML = "O melhor supermercado para si é o Continente";
        document.getElementById("bestValue").innerHTML = " com um valor total de " + continente_total_price_string + "!";
    }
    if(jumbo_total_price < continente_total_price && jumbo_total_price < pingoDoce_total_price && userPrefs.includes(jumbo_id)){
        document.getElementById("supermercado").innerHTML = "O melhor supermercado para si é o Jumbo";
        document.getElementById("bestValue").innerHTML = " com um valor total de " + jumbo_total_price_string+ "!";
    }
}

function showMissingItems(){
    //Pingo Doce
    var finalHTML = "";
    var divID = "missingContent";
    if(pingoDoce_item_id_missing.length){

        var tempHTML = "";

        tempHTML += "<p><span>Produtos em falta no PingoDoce:</span><br>";
        for(i = 0; i < pingoDoce_item_id_missing.length; i++){
            tempHTML += "\n <span>- " + pingoDoce_item_name_missing[i] + "</span><br>";
        }
        finalHTML += "\n" + tempHTML+"</p>";
    }

    if(continente_item_id_missing.length){

        var tempHTML = "";

        tempHTML += "<p><span>Produtos em falta no Continente:</span><br>";
        for(i = 0; i < continente_item_name_missing.length; i++){
            tempHTML += "\n <span>- " + continente_item_name_missing[i] + "</span><br>";
        }
        finalHTML += "\n" + tempHTML +"</p>";
    }

    if(jumbo_item_id_missing.length){

        var tempHTML = "";

        tempHTML += "<p><span>Produtos em falta no Jumbo:</span><br>";
        for(i = 0; i < jumbo_item_id_missing.length; i++){
            tempHTML += "\n <span>- " + jumbo_item_name_missing[i] + "</span><br>";
        }
        finalHTML += "\n" + tempHTML+"</p>";
    }
    document.getElementById("missingContent").innerHTML = finalHTML;

}



//Function to calculate total prices from each store
function totalPrices(){
    if(userPrefs.includes(pingoDoce_id)){
        for(i = 0; i < pingoDoce_item_id.length; i++){
            pingoDoce_total_price += pingoDoce_item_price[i];
        }
        pingoDoce_total_price_string = pingoDoce_total_price.toFixed(2).toString() + "€";
    }
    else{
        pingoDoce_total_price_string = "-";
    }

    if(userPrefs.includes(continente_id)){
        for(i = 0; i < continente_item_id.length; i++){
            continente_total_price += continente_item_price[i];
        }
        continente_total_price_string = continente_total_price.toFixed(2).toString() + "€";
    }
    else{
        continente_total_price_string = "-";
    }

    if(userPrefs.includes(jumbo_id)){
        for(i = 0; i < jumbo_item_id.length; i++){
            jumbo_total_price += jumbo_item_price[i];
        }
        jumbo_total_price_string = jumbo_total_price.toFixed(2).toString() + "€";
    }
    else{
        jumbo_total_price_string = "-";
    }
}

//

function itemsUniqueDict(){
    var FL = globalResponseData['itemCounters']['FL'];
    var CL = globalResponseData['itemCounters']['CL'];
    var BD = globalResponseData['itemCounters']['BD'];
    var MC = globalResponseData['itemCounters']['MC'];
    var LT = globalResponseData['itemCounters']['LT'];
    var CP = globalResponseData['itemCounters']['CP'];
    var BS = globalResponseData['itemCounters']['BS'];
    var CQ = globalResponseData['itemCounters']['CQ'];

    var itemCounter = 0;
    //var counter = 0;


    if(FL > 0){
        for(i = 0; i < FL; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Frutas e Legumes']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(CL > 0){
        for(i = 0; i < CL; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Congelados']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Congelados']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Congelados']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Congelados']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(BD > 0){
        for(i = 0; i < BD; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bebidas']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(MC > 0){
        for(i = 0; i < MC; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Mercearia']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(LT > 0){
        for(i = 0; i < LT; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Lacticínios']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(CP > 0){
        for(i = 0; i < CP; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Carne e Peixe']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(BS > 0){
        for(i = 0; i < BS; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Bolachas e Doces']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }

    if(CQ > 0){
        for(i = 0; i < CQ; i++){
            fullItemDict[prefix + itemCounter.toString()] =  {};
            fullItemDict[prefix + itemCounter.toString()]['itemID'] = globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['itemID'];
            fullItemDict[prefix + itemCounter.toString()]['itemName'] = globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['itemName'];
            fullItemDict[prefix + itemCounter.toString()]['itemQuantity'] = globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['itemQuantity'];
            fullItemDict[prefix + itemCounter.toString()]['storeArray'] = []
            fullItemDict[prefix + itemCounter.toString()]['priceArray'] = []
            if(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice0']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice0']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice0']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice1']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice1']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice1']['itemPrice']);
            }
            if(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice2']['exists'] == true){
                fullItemDict[prefix + itemCounter.toString()]['storeArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice2']['storeID']);
                fullItemDict[prefix + itemCounter.toString()]['priceArray'].push(globalResponseData['productCatList']['Charcutaria e Queijos']['item' + i.toString()]['pricesStores']['storePrice2']['itemPrice']);
            }
            itemCounter += 1;
        }
    }
    fullItemDict['totalItems'] = itemCounter;

}