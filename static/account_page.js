form_fields = ["org_name", "email", "phone", "account_number", "routing_number", "bank_name", "st_and_apt", "city", "state", "zipcode", "country"]

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
        //TODO replace temp object with account_info
        $("#"+x).html(account_info[x])
    }
}


$("#document").ready(function() {
    load_info()

    //TODO:
    //1. edit button routes to edit_page.html which isn't complete yet
})