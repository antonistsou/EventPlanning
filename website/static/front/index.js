$(document).ready(function(){   
        var array = new Array();
        var priorArray = new Array();

        var buttons = document.getElementsByClassName("btn btn-outline-primary")
        var map = new Map();
      
        const buttonPressed = e => {
          
            btnID = e.target;  // Get ID of Clicked Element
            var flag = true
  
            if(!array.includes(btnID.id))
            {
                btnID.textContent = 'Selected!';
                // btnID.style.background = 'light green';
                array.push(btnID.id);
                flag = false;
            }
            
            if(flag){  
                btnID.textContent = 'Select';
                // btnID.style.background = 'green';
                for( var i = 0; i < array.length; i++){ 
                    if ( array[i] == btnID.id) { 
                        array.splice(i, 1); 
                        slice= i;
                    }
                }
            }
            var radiochecked = document.querySelector('input[type="radio"][name="priority' + btnID.id + '"]:checked');
            var intid =radiochecked.id;
           
            intid= intid - btnID.id*btnID.id;
            
        
            if(!flag){
                priorArray.push(intid);
                for(var i = 0; i< array.length ; i++){
                  map.set(array[i], priorArray[i]);
                }
            }            
            else{
                priorArray.splice(slice, 1);     
                map.delete(btnID.id)
            }

            // console.log("Select array : "+array);
            // console.log("Priority array : "+priorArray);
        
         
            console.log(map);  
          
        }

        function sendMapToServer() {
            const data = JSON.stringify({ 'map': [...map] });
            fetch('/result', {
              method: 'POST',
              body: data,
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then(response => {
              console.log(response);
              window.location.href = '/result';
            })
            .catch(error => {
              console.log('Error sending data');
            });
          }
          
          $(".btn-primary").on('click', function() {
            sendMapToServer();
          });

        for (let button of buttons) {
            
              button.addEventListener("click", buttonPressed);
           
        }
       
})
       
