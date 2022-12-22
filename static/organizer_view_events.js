// {"event_id": 1, 
// "name": "Tree lighting", 
// "organizer_id": "1", 
// "date": "2022-12-23", 
// "start_time": "11:00:00", 
// "end_time": "14:00:00", 
// "description": "A Christmas tree lighting!", 
// "event_category": "Holiday", 
// "capacity": 50, 
// "image_url": null}

function event_template(event){


}

function insert_events(event_list){
    $("#list_events").empty()

    for(const event of event_list){
        event_template(event)
    }
}

function fetch_events(start, end){
    //Ajax for fetching events based on start and end with pagination
    let event_list = {}
}

$("#document").ready(function() {
    $("#button").click(function{
        fetch_events(start, end)
    })
})