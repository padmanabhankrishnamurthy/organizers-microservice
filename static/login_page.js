form_fields = ["username", "password"]

function send_login_cred(){
    // TODO
    // 1. AJAX call to autheticate if credentials are correct. then redirect to account page
    // 2. If incorrect credentials, empty form and ask to submit again
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

    $("#login-form").submit(function(e){
        e.preventDefault()

        var valid = true

        for(const x of form_fields){
            if(($("#"+x).val() == null || $("#"+x).val() =="")){
                valid = false
            }
        }

        if(valid){
            send_login_cred()
        }
    })
})