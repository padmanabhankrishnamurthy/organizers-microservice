form_fields = ["org_name", "email", "phone", "account_number", "routing_number", "bank_name", "st_and_apt", "city", "state", "zipcode", "country"]
// let SUBMIT_ENDPOINT = "http://organizers-microservice-env.eba-sbvxbuwq.us-east-1.elasticbeanstalk.com/"
let SUBMIT_ENDPOINT = "https://127.0.0.1:5000/"
let ACCOUNT_PAGE_URL = "https://127.0.0.1:5000/account_page"

function submit_signup(){
    var data = {}

    for(const x of form_fields){
        data[x] = $("#"+x).val()
    }
    data["non_profit"] = $("#non_profit").is(":checked")

    // TODO:
    // 1. add username and password fields
    // 2. check if username is taken
    //        if taken, ask to enter a different username. Need to check success in ajax function
    //        else create account and lof it in db
    $.ajax({
      type: "POST",
      url: SUBMIT_ENDPOINT + "onboard_api",
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      success: function(result) {
        var org_id = result["org_id"]
        window.location.href = ACCOUNT_PAGE_URL
      }
  });

    console.log(data)
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

    $("#signup-form").submit(function(e){
        e.preventDefault()

        var valid = true

        for(const x of form_fields){
            if(($("#"+x).val() == null || $("#"+x).val() =="")){
                valid = false
            }
        }

        if(valid){
            submit_signup()
        }

        console.log("func end")
    })
})