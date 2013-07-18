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

var SparklineSet = function(container$, options){
    this.options = options
    this.container$ = container$
    this.init()
}
SparklineSet.prototype = {
    init: function(){
        console.log("init IsaSparkline")
    }
    ,createSparklineBar: function(container$, values){
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


        container$.find("span.primary span.value").html(options.primaryNum)
        container$.find("span.secondary span.value").html(options.secondaryNum)
        container$.find("span.sparkline").sparkline(values, options)
    }
    ,createSparklineLine: function(name, xValues, yValues){
        var weekDays = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        var defaultOptions = {
            iaPrimaryValue: _.last(yValues),
            iaPrimaryValueLabel:'',
            iaSecondaryValue: _.max(yValues),
            iaSecondaryValueLabel: "max",
            iaHref: "#",
            iaName: name,
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
        var elem$ = ich.sparklineWithNumbers(options)

        this.container$.find("div.container").append(elem$)
        this.container$.find(".sparkline."+name).sparkline(yValues, options)

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