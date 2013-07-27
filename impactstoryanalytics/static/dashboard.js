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

/*******************************************************************************
 *
 *  ok, option precedence goes like this, from least to greatest precedence:
 *  Sparkline.defaultOptions
 *  Sparkline.typeSpecificOptions
 *  Sparkline.unitSpecificOptions
 *  SparklineSet.userSuppliedOptions
 *  SparklineSet.calculatedOptions (including yValues from rows + sparkline classNames)
 *  Sparkline.userSuppliedOptions
 *  Sparkline.calculatedOptions
 *
 ******************************************************************************/





var SparklineSet = function(rows, optionsFromUser){
    this.rows = rows
    this.optionsFromUser = optionsFromUser



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
    calculateSSOptions: function(){
        var calculatedOptions = _.clone(this.optionsFromUser, {})

        calculatedOptions.xvalues = _.map(_.pluck(this.rows, "start_iso"), function(iso){
            return moment(iso).format("X")
        })

        calculatedOptions.iaShareYAxisMax = this.findOverallMax()

        return calculatedOptions
    }
    ,addSparkline: function(sparkline){
        var calculatedOptions = this.calculateSSOptions()

        sparkline.setOptions.call(sparkline, calculatedOptions, this.rows)
        this.sparklines.push(sparkline)
    }
    ,findOverallMax: function(){
        var overallMax = 0
        _.each(this.sparklines, function(s){
            if (s.options.iaShareYAxis) {
                var thisSparklineMax = _.max(s.options.iaYvalues)

                overallMax = _.max([thisSparklineMax, overallMax])
            }
        })
        return overallMax
    }
    ,render: function(loc$) {
        var that = this
        var max = this.findOverallMax()
        _.each(this.sparklines, function(sparkline){
            sparkline.setYAxisMaxIfShared(max)
            sparkline.render(loc$, that.calculatedOptions, that.rows)
        })
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
        iaShareYAxis: false,
        iaUnit: "default",
        type: "line",
        width: "150px",
        iaHighlight: false,
        iaBorderTop: false
    }
    this.userSuppliedOptions = userSuppliedOptions
    this.options = {}

}
Sparkline.prototype = {
    typeSpecificDefaultOptions: function(type){
        type = type || "line"
        var defaultOptions = {
            bar:{
                iaPrimaryValue: function(values){
                    console.log("reducing values, got these: ", values)
                    return _.reduce(values, function(memo, num) { return memo + num})
                },
                iaSecondaryValue: function(values) {return _.max(values)},
                tooltipFormatter: function(sparkline, options, fields) {
                    return "still working on it..."
                },
                type:"bar",
                barWidth: 2
            },
            line: {
                iaPrimaryValue: function(yValues) {return Math.round(_.last(_.without(yValues, null)))},
                iaSecondaryValue: function(yValues) {return Math.round(_.max(yValues))},
                type:"line",
                tooltipFormatter:function(sparkline, options, fields){
                    var dateStr = moment(fields.x*1000).format("MMM D")
                    return "<span>" + Math.round(fields.y) + '</span>' + ', ' + dateStr
                }
            }
        }
        return defaultOptions[type]
    }
    ,unitSpecificDefaultOptions: function(unit){
        unit = unit || "default"

        return {
            percent: {
                lineColor: "indianred",
                fillColor: "pink",
                iaPrimaryUnit: "%",
                iaSecondaryUnit: "%",
                chartRangeMax: 100
            },
            default: {}
        }[unit]
    }
    ,render: function(container$){
        var elem$ = ich.sparklineWithNumbers(this.options)
        container$.find("div.container").append(elem$)
        container$.find(".sparkline."+this.options.iaClassName)
            .sparkline(this.options.iaYvalues, this.options)
        return container$
    }
    ,setOptions: function(extraOptions, dataRows){

        // start with the custom user options handed to us at instantiation
        var options = _.clone(this.userSuppliedOptions)


        // apply extra options handed in to us at render time (likely from a SparklineSet)
        options = _.defaults(options, extraOptions)


        // layer on type-specific options
        options = _.defaults(
            options,
            this.typeSpecificDefaultOptions(options.type) // gets overwritten if conflicts
        )

        // layer on with unit-specific options
        options = _.defaults(
            options,
            this.unitSpecificDefaultOptions(options.iaUnit) // gets overwritten if conflicts
        )

        // layer on any default options not covered yet:
        // start with the default options
        options = _.defaults(options, this.defaultOptions)


        // finally, calculate new values based on stuff we've put in the options
        options = this.calculateOptions(options, dataRows)

        // done!
        this.options = options



    }
    ,calculateOptions: function(options, dataRows) {
        // calculate yvalues
        if (!options.iaYvalues) {
            options.iaYvalues = _.pluck(dataRows, options.iaClassName)
        }

        // run the functions defined in options, and replace them with their values.
        var primaryValue = options.iaPrimaryValue.call(this, options.iaYvalues)
        var secondaryValue = options.iaSecondaryValue.call(this, options.iaYvalues)

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
    ,setYAxisMaxIfShared: function(max){
        if (this.options.iaShareYAxis) {
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