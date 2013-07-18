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

// OBJECTS

var IsaSparkline = function(options){
    this.options = options
    this.init()
}
IsaSparkline.prototype = {
    init: function(){
        console.log("init IsaSparkline")
    }
    ,createSparklineBar: function(loc$, values){
        var defaultOptions = {
            primaryNum: _.reduce(values, function(memo, num) { return memo + num}),
            primaryNumLabel:'',
            secondaryNum: _.max(values),
            secondaryNumLabel: "max",
            tooltipFomatter: function(sparkline, options, fields) {
                return "still working on it..."
            },
            type:"bar",
            chartRangeMin:0,
            barWidth: 2
        }
        var options = _.extend(defaultOptions, this.options)


        loc$.find("span.primary span.value").html(options.primaryNum)
        loc$.find("span.secondary span.value").html(options.secondaryNum)
        loc$.find("span.sparkline").sparkline(values, options)
    }
    ,createSparklineLine: function(loc$, xValues, yValues){
        var weekDays = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        var defaultOptions = {
            primaryNum: _.last(yValues),
            primaryNumLabel:'',
            secondaryNum: _.max(yValues),
            secondaryNumLabel: "max",
            type:"line",
            maxSpotColor: false,
            minSpotColor: false,
            spotColor: false,
            chartRangeMin:0,
            xvalues: xValues,
            tooltipFormatter:function(sparkline, options, fields){
                var d = new Date(fields.x * 1000)
                var mins = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes()
                var dateStr = weekDays[d.getDay()] + ' ' + d.getHours() + ':' + mins
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var options = _.extend(defaultOptions, this.options)


        loc$.find("span.primary span.value").html(options.primaryNum)
        loc$.find("span.secondary span.value").html(options.secondaryNum)
        loc$.find("span.sparkline").sparkline(yValues, options)

    }
}




// PROCEDURAL CODE
$(document).ready(function(){

    _.each(widgetNames, function(name){
        var widget = new window[capitalize(name)]()
        var dataUrl = "/widget_data/"+name
        load_widget_data(widget, dataUrl)
    })

})