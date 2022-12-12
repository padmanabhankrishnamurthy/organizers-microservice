form_fields = ["org_name", "email", "phone", "account_number", "routing_number", "bank_name", "st_and_apt", "city", "state", "zipcode", "country"]
var BASE_URL = "http://127.0.0.1:5000/"
var EDIT_PAGE_URL = BASE_URL + "edit_page/"
var DELETE_ENDPOINT = BASE_URL + "delete_account_api"

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
    "country": "USA"
}

function load_info(){
    for (const x of form_fields){
        $("#"+x).html(account_info[x])
    }
}

function delete_account(){
    var org_id = window.location.href.split("/").at(-1)

    $.ajax({
        type: "POST",
        url: DELETE_ENDPOINT,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({"org_id":org_id}),
        success: function(result) {
            // TODO: logout
            window.location.href = BASE_URL
        }
      });
}

function edit_page(){
    var org_id = window.location.href.split("/").at(-1)
    window.location.href = EDIT_PAGE_URL + org_id
}

$("#document").ready(function() {
    load_info()

    $("#edit_info").click(function(){
        edit_page()
    })

    $("#delete_account").click(function() {
        delete_account()
    })
})