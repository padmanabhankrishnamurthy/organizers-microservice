form_fields = ["org_name", "email", "phone", "account_number", "routing_number", "bank_name", "st_and_apt", "city", "state", "zipcode", "country"]
// let SUBMIT_ENDPOINT = "http://organizers-microservice-env.eba-sbvxbuwq.us-east-1.elasticbeanstalk.com/"
let SUBMIT_ENDPOINT = "http://127.0.0.1:5000/"

var temp_object = {
    "org_name": "apple", 
    "email": "apple@apple.com", 
    "phone": "78923492203", 
    "account_number": "2983211", 
    "routing_number": "AVAB20923", 
    "bank_name": "Chase", 
    "st_and_apt": "155 claremeont", 
    "city": "New York", 
    "state": "NY", 
    "zipcode": "10027", 
    "country": "USA",
    "non_profit": true
}

function submit_edit(){
    var data = {}

    for(const x of form_fields){
        data[x] = $("#"+x).val()
    }
    data["non_profit"] = $("#non_profit").is(":checked")

    // AJAX edit info endpoint
    // $.ajax({
    //   type: "POST",
    //   url: SUBMIT_ENDPOINT + "onboard_api",
    //   dataType: "json",
    //   contentType: "application/json; charset=utf-8",
    //   data: JSON.stringify(data)
    // });

    console.log(data)
}

function load_info(){
    for (const x of form_fields){
        //TODO replace temp object with account_info
        $("#"+x).val(temp_object[x])
    }
    $('#non_profit').prop('checked', temp_object["non_profit"]);
}

$("#document").ready(function() {
    (function () {
        'use strict'
      
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')
      
        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
          .forEach(function (form) {
            form.addEventListener('submit', function (event) {
              if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
              }
      
              form.classList.add('was-validated')
            }, false)
          })
    })()

    load_info()

    $("#edit-form").submit(function(e){
        e.preventDefault()

        var valid = true

        for(const x of form_fields){
            if(($("#"+x).val() == null || $("#"+x).val() =="")){
                valid = false
            }
        }

        if(valid){
            submit_edit()
        }

        console.log("func end")
    })
})