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

var SparklineSet = function(container$, options){
    var defaultOptions = {
        iaPrimaryValueLabel:'',
        iaSecondaryValueLabel: "max",
        iaHref: "#",
        maxSpotColor: false,
        minSpotColor: false,
        spotColor: false,
        iaLabelWidth: "1",
        chartRangeMin:0
    }
    this.options = _.extend(defaultOptions, options)
    this.container$ = container$
    this.init()
}
SparklineSet.prototype = {
    init: function(){
        console.log("init IsaSparkline")
    }
    ,createSparklineBar: function(name, values){
        var reduce = function(values){
            return _.reduce(values, function(memo, num) { return memo + num})
        }
        var defaultOptions = {
            iaPrimaryValue: reduce,
            iaSecondaryValue: function(values) {return _.max(values)},
            tooltipFomatter: function(sparkline, options, fields) {
                return "still working on it..."
            },
            type:"bar",
            iaName: name,
            iaDisplayName: name,
            barWidth: 2
        }
        var options = this.optionsForDisplay(defaultOptions, this.options, [values])
        this.renderSparkline(name, values, options)

    }
    ,createSparklineLine: function(name, xValues, yValues){
        var defaultOptions = {
            iaPrimaryValue: function(xValues, yValues) {return _.last(yValues)},
            iaSecondaryValue: function(xValues, yValues) {return _.max(yValues)},
            iaName: name,
            iaDisplayName: name,
            type:"line",
            xvalues: xValues,
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment(fields.x*1000).format("MMM D")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var options = this.optionsForDisplay(defaultOptions, this.options, [xValues, yValues])
        this.renderSparkline(name, yValues, options)

    }
    ,renderSparkline: function(name, values, options) {
        var elem$ = ich.sparklineWithNumbers(options)
        this.container$.find("div.container").append(elem$)
        this.container$.find(".sparkline."+name).sparkline(values, options)
    }
    ,optionsForDisplay: function(defaultOptions, newOptions, args){
        var options = _.extend(defaultOptions, newOptions)

        // run the functions defined here, and replace them with their values.
        var primaryValue = options.iaPrimaryValue.apply(this, args)
        var secondaryValue = options.iaSecondaryValue.apply(this, args)

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