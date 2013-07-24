// UTILITY FUNCTIONS

function capitalize(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function nFormatter(num) {
    // from http://stackoverflow.com/a/14994860/226013
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
    }
    return num;
}

// PAGE FUNCTIONS

function load_widget(widget, dataUrl) {
    // first load the data, then use it to creat the widget
    $.ajax({
               url: dataUrl,
               type:"GET",
               success: function(data){
                       widget.create.call(widget, data)
               }
           })
}

// OBJECTS
var SparklineSet = function(baseOptions){
    this.baseOptions = baseOptions
    this.init()
    this.sparklines = []
}
SparklineSet.prototype = {
    init: function(){
        console.debug("SparklineSet init")
    }
    ,addSparkline: function(values, newOptions){
        var options = _.extend(this.baseOptions, newOptions)
        this.sparklines.push(new Sparkline(values, options))
    }
    ,render: function(loc$) {
        _.each(this.sparklines, function(sparkline){
            console.debug("rendering sparkline now: ", sparkline.options.iaDisplayName)
            sparkline.render(loc$)
        })
    },
    findOverallMax: function(){

    }
}


var Sparkline = function(yValues, options){
    var defaultOptions = {
        iaClassName: "generic",
        iaHref: "#",
        iaDisplayName: "Generic widget",
        iaPrimaryValueLabel:'',
        iaSecondaryValueLabel: "max",
        maxSpotColor: false,
        minSpotColor: false,
        spotColor: false,
        iaLabelWidth: "1",
        chartRangeMin:0,
        type: "line"
    }
    this.options = _.extend(defaultOptions, options)
    this.yValues = yValues
    this.init()
}
Sparkline.prototype = {
    init: function(){
        console.log("init sparkline")
    }
    ,defaultOptionsByType: function(type){
        var reduce = function(values){
            return _.reduce(values, function(memo, num) { return memo + num})
        }
        var defaultOptions = {
            bar:{
                iaPrimaryValue: reduce,
                iaSecondaryValue: function(values) {return _.max(values)},
                tooltipFormatter: function(sparkline, options, fields) {
                    return "still working on it..."
                },
                type:"bar",
                barWidth: 2
            },
            line: {
                iaPrimaryValue: function(yValues) {return _.last(yValues)},
                iaSecondaryValue: function(yValues) {return _.max(yValues)},
                type:"line",
                tooltipFormatter:function(sparkline, options, fields){
                    var dateStr = moment(fields.x*1000).format("MMM D")
                    return "<span>" + fields.y + '</span>' + ', ' + dateStr
                }
            }
        }
        return defaultOptions[type]
    }
    ,render: function(container$){
        var typeAwareOptions = _.extend(
            this.defaultOptionsByType(this.options.type),
            this.options
        )
        console.log("set type-aware options: ", typeAwareOptions)

        var options = this.optionsForDisplay(typeAwareOptions)
        console.log("set options for display: ", options)

        var elem$ = ich.sparklineWithNumbers(options)
        container$.find("div.container").append(elem$)
        container$.find(".sparkline."+options.iaClassName).sparkline(this.yValues, options)
        return container$
    }
    ,optionsForDisplay: function(options){

        // run the functions defined here, and replace them with their values.
        var primaryValue = options.iaPrimaryValue.call(this, this.yValues)
        var secondaryValue = options.iaSecondaryValue.call(this, this.yValues)

        options.iaPrimaryValue = primaryValue
        options.iaSecondaryValue = secondaryValue

        // format primary and secondary values for display
        options.iaPrimaryValueDisplay = nFormatter(primaryValue)
        options.iaSecondaryValueDisplay = nFormatter(secondaryValue)
        return options
    }
}




// PROCEDURAL CODE
$(document).ready(function(){

    _.each(widgetNames, function(name){
        console.log("Now running the '"+ name + "' widget")
        var widget = new window[capitalize(name)]()
        var dataUrl = "/widget_data/"+name
        load_widget(widget, dataUrl)
    })

})