

$(document).ready(function(){   
        var array = new Array();
        $(".btn").on('click',function(){
            var flag = true
            var btnID = document.getElementById(this.id);
            if(!array.includes(this.id))
            {
            btnID.textContent = 'Selected!';
            btnID.style.background = 'light green';
            array.push(this.id);
            flag = false;
            }
            
            if(flag){  
                btnID.textContent = 'Select';
                btnID.style.background = 'green';
            for( var i = 0; i < array.length; i++){ 

                if ( array[i] == this.id) { 
                    array.splice(i, 1); 
                }
                }
            }
            console.log(array);})
        $(".btn-primary").on('click',function(){
            sessionStorage.setItem('array' , JSON.stringify(array));
            window.location.href="/result";
            })
          
         })

 
