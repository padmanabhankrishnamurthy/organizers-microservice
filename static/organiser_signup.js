form_fields = ["org_name", "email", "account_number", "routing_number", "bank_name", "st_and_apt", "city", "state", "zipcode", "country"]

function submit_signup(){
    var data = {}

    for(const x of form_fields){
        data[x] = $("#"+x).val()
    }
    data["non_profit"] = $("#non_profit").is(":checked")

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