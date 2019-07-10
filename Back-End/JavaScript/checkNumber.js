 function checkNumber(number){
     
            carrier = ["1","2","3","6"];
            
            if(number[0] != 9 ){
                return false;
            }

            if(number.length != 9){
                return false;
            }

            if(!(carrier.includes(number[1]))){
                return false;
            }

            return true;            

}