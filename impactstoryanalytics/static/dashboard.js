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






/*******************************************************************************
*
*  OBJECTS
*
******************************************************************************/


var SparklineSet = function(rows, baseOptions){
    this.baseOptions = baseOptions
    this.rows = rows
    this.sparklines = []
    this.init()
}
// static method
SparklineSet.conversionRate = function(rows, numeratorKey, denominatorKey){
    return _.map(rows, function(row){
        if (!row[denominatorKey]) { // no dividing by zero
            return null
        }
        else {
            return Math.round(100 * row[numeratorKey] / row[denominatorKey])
        }
    })
}
SparklineSet.prototype = {
    init: function(){
        console.debug("SparklineSet init")
        this.baseOptions.xvalues = _.map(_.pluck(this.rows, "start_iso"), function(iso){
            return moment(iso).format("X")
        })
    }
    ,addSparkline: function(sparkline){
        _.extend(sparkline.options, this.baseOptions)

        var yValues = _.pluck(this.rows, sparkline.options.iaClassName)

        if (!sparkline.options.iaYvalues.length) {
            sparkline.options.iaYvalues = yValues
        }
        this.sparklines.push(sparkline)
    }
    ,render: function(loc$) {
        var max = this.setOverallMax()
        _.each(this.sparklines, function(sparkline){
            sparkline.setYAxisIfShared.call(sparkline, max)
            sparkline.render(loc$)
        })
    },
    setOverallMax: function(){
        this.overallMax = 0
        _.each(this.sparklines, function(s){
            if (s.iaShareYAxis) {
                var thisSparklineMax = _.max(s.iaYvalues)
                this.overallMax = _.max(thisSparklineMax, this.overallMax)
            }
        })
        return this.overallMax
    }
}


var Sparkline = function(userSuppliedOptions){
    this.defaultOptions = {
        iaClassName: false,
        iaHref: "#",
        iaDisplayName: false,
        iaPrimaryValueLabel:'',
        iaSecondaryValueLabel: "max",
        maxSpotColor: false,
        minSpotColor: false,
        spotColor: false,
        iaLabelWidth: "1",
        chartRangeMin:0,
        sharedYAxis: false,
        type: "line",
        iaYvalues: []
    }
    this.options = false
    this.init(userSuppliedOptions)
}
Sparkline.prototype = {
    init: function(userSuppliedOptions){
        var typeAwareOptions = _.extend(
            this.defaultOptions,
            this.typeSpecificDefaultOptions(userSuppliedOptions.type)
        )
        this.options = _.extend(typeAwareOptions, userSuppliedOptions)
    }
    ,typeSpecificDefaultOptions: function(userDefinedType){
        var type = userDefinedType || this.defaultOptions.type

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

        var options = this.optionsForDisplay(this.options)

        var elem$ = ich.sparklineWithNumbers(options)
        container$.find("div.container").append(elem$)
        container$.find(".sparkline."+options.iaClassName).sparkline(this.options.iaYvalues, options)
        return container$
    }
    ,optionsForDisplay: function(options){

        // run the functions defined here, and replace them with their values.
        var primaryValue = options.iaPrimaryValue.call(this, this.options.iaYvalues)
        var secondaryValue = options.iaSecondaryValue.call(this, this.options.iaYvalues)

        options.iaPrimaryValue = primaryValue
        options.iaSecondaryValue = secondaryValue

        // format primary and secondary values for display
        options.iaPrimaryValueDisplay = nFormatter(primaryValue)
        options.iaSecondaryValueDisplay = nFormatter(secondaryValue)

        if (!options.iaDisplayName){
            options.iaDisplayName = options.iaClassName.replace(/[-_]/g, " ")
        }

        return options
    }
    ,setYAxisIfShared: function(max){
        if (this.sharedYAxis){
            this.options.chartRangeMax = max
            return true
        }
        else {
            return false
        }
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