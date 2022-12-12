$(document).ready(function(){
    
    var array = new Array();
        $(".btn").on('click',function(){
            var flag = true
            var btnID = document.getElementById(this.id);
            if(!array.includes(btnID))
            {
              btnID.textContent = 'Selected!';
              btnID.style.background = 'light green';
              array.push(btnID);
              flag = false;
            }
            
            if(flag){  
                btnID.textContent = 'Select';
                btnID.style.background = 'green';
            for( var i = 0; i < array.length; i++){ 

                if ( array[i] == btnID) { 
                    array.splice(i, 1); 
                }
                }
            }

            console.log(array);
          })
    })