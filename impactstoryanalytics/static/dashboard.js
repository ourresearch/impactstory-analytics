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
    this.rows = rows
    this.baseOptions = this.loadBaseOptions(baseOptions)
    this.sparklines = []
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
    loadBaseOptions: function(baseOptions){
        baseOptions.xvalues = _.map(_.pluck(this.rows, "start_iso"), function(iso){
            return moment(iso).format("X")
        })
        return baseOptions
    }
    ,addSparkline: function(sparkline){
        sparkline.options = _.extend(sparkline.options, this.baseOptions)

        if (!sparkline.yValues.length) {
            /* if the user hasn't set their own y values, pluck them from the
            *  supplied rows, using the iaClassName option for the key
            */
            sparkline.yValues = _.pluck(this.rows, sparkline.options.iaClassName)
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
        var overallMax = 0
        _.each(this.sparklines, function(s){
            if (s.options.iaShareYAxis) {
                var thisSparklineMax = _.max(s.yValues)

                overallMax = _.max([thisSparklineMax, overallMax])
            }
        })
        this.overallMax = overallMax
        return this.overallMax
    }
}


var Sparkline = function(userSuppliedOptions){
    var defaultOptions = {
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
        iaShareYAxis: false,
        iaUnit: "default",
        type: "line"
    }
    this.options = this.setOptions(defaultOptions, userSuppliedOptions)
    this.yValues = userSuppliedOptions.iaYvalues || []

}
Sparkline.prototype = {
    setOptions: function(defaultOptions, userSuppliedOptions){

        // this is ugly, should be fixed:
        var type  = userSuppliedOptions.type || defaultOptions.type
        var unit = userSuppliedOptions.iaUnit || defaultOptions.iaUnit


        // first extend with type-specific options, using type supplied by user
        var options = _.extend(
            defaultOptions,
            this.typeSpecificDefaultOptions(type)
        )

        // extend with unit-specific options (mostly colors)
        options = _.extend(
            options,
            this.unitSpecificDefaultOptions(unit)
        )

        // finally, apply whatever options the user supplied
        return _.extend(options, userSuppliedOptions)
    }
    ,typeSpecificDefaultOptions: function(userDefinedType){
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
                iaPrimaryValue: function(yValues) {return _.last(_.compact(yValues))},
                iaSecondaryValue: function(yValues) {return _.max(yValues)},
                type:"line",
                tooltipFormatter:function(sparkline, options, fields){
                    var dateStr = moment(fields.x*1000).format("MMM D")
                    return "<span>" + fields.y + '</span>' + ', ' + dateStr
                }
            }
        }
        return defaultOptions[userDefinedType]
    }
    ,unitSpecificDefaultOptions: function(unit){
        return {
            percent: {
                lineColor: "indianred",
                fillColor: "pink",
                iaPrimaryUnit: "%",
                iaSecondaryUnit: "%"
            },
            default: {}
        }[unit]
    }
    ,render: function(container$){

        var options = this.optionsForDisplay(this.options)

        var elem$ = ich.sparklineWithNumbers(options)
        container$.find("div.container").append(elem$)
        container$.find(".sparkline."+options.iaClassName).sparkline(this.yValues, options)
        return container$
    }
    ,optionsForDisplay: function(options){

        // run the functions defined in options, and replace them with their values.
        var primaryValue = options.iaPrimaryValue.call(this, this.yValues)
        var secondaryValue = options.iaSecondaryValue.call(this, this.yValues)


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
        if (this.options.iaShareYAxis){
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