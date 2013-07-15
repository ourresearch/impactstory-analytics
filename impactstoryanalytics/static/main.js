function load_widget_data(widget) {
    console.log("here's where i'll get data from ", widget.dataUrl)
    $.ajax({
               url: widget.dataUrl,
               type:"GET",
               success: function(data){
                       widget.create.call(widget, data)
               }
           })


}


$(document).ready(function(){


})