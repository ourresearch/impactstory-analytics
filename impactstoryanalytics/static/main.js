// UTILITY FUNCTIONS

function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}


// PAGE FUNCTIONS

function load_widget_data(widget, dataUrl) {
    $.ajax({
               url: dataUrl,
               type:"GET",
               success: function(data){
                       widget.create.call(widget, data)
               }
           })
}


// PROCEDURAL CODE
$(document).ready(function(){

    _.each(widgetNames, function(name){
        var widget = new window[capitalize(name)]()
        var dataUrl = "/widget_data/"+name
        load_widget_data(widget, dataUrl)
    })

})