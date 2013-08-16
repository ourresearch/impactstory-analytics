// page globals
function color(color, value){
    var colors = {
        'scalar': "#3498db",
        'percent': "#2ecc71"
    }
    if (color == 'default') {
        color = 'scalar'
    }
    var myColor = colors[color]
    if (value == "light"){
        myColor = tinycolor.lighten(myColor, 40).toHexString()
    }
    else if (value == "medium") {
        myColor = tinycolor.lighten(myColor, 20).toHexString()
    }
    return myColor
}

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

function log10(val) {
    if (val === 0) {
        return 0
    }
    else {
        return Math.log(val) / Math.LN10;
    }

}

function makeObjFromName(name){
    var obj = new window[capitalize(name)]()
    obj.name = name  // loathsome hack arg
    return obj

}

// PAGE FUNCTIONS

function load_widget(widget, dataUrl) {
    function log(msg) { return console.log(widget.name + ": " + msg)}

    // first load the data, then use it to create the widget
    log("now running.")

    $.ajax({
               url: dataUrl,
               type:"GET",
               success: function(data){
                   log("got data back from REST call; rendering.")
                   widget.create.call(widget, data)
               }
           })
}
function PagesController(loc){
    this.loc = loc
    this.init()
    this.refreshTime = 60*2 // every two minutes
}
PagesController.prototype = {
    init: function(){
        var that = this
        var pageMethodName = this.loc.pathname.slice(1) + "Page"
        if (pageMethodName in this) {
            this[pageMethodName]()
        }
        this.allPages()
        setTimeout(function(){that.init.call(that)}, that.refreshTime*1000)
    }
    ,todayPage: function(){
        console.log("welcome to the today page!")
    }
    ,allPages: function() {
        var that = this
        _.each(widgetNames, function(name){
            var widget = makeObjFromName(name)
            var dataUrl = "/widget_data/"+name
            load_widget(widget, dataUrl)
        })
    }
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
    this.summarySparklines = [] // these print at the bottom
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
    ,addSparkline: function(sparkline, isSummary){
        var that = this
        var calculatedOptions = this.calculateSSOptions()

        sparkline.setOptions.call(sparkline, calculatedOptions, that.rows)
        if (isSummary) {
            this.summarySparklines.push(sparkline)
        }
        else {
            this.sparklines.push(sparkline)
        }
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
        var container$ = loc$.find(".container")
        container$.empty()
        _.each(this.sparklines, function(sparkline){
            sparkline.setYAxisMaxIfShared(max)
            sparkline.render(container$, that.calculatedOptions, that.rows)
        })
        _.each(this.summarySparklines, function(sparkline){
            sparkline.render(container$, that.calculatedOptions, that.rows)
        })
    }
    ,sortBy: function(sortBy){
        sortBy = sortBy || "max"
        that = this
        if (sortBy=="max"){
            this.sparklines = _.sortBy(that.sparklines, function(sparkline){
                return _.max(sparkline.options.iaYvalues)
            }).reverse()
        }

        return this
    }
    ,first: function(size) {
        this.sparklines = this.sparklines.slice(0, size)
        return this
    }
    ,addTotalSparkline: function(options){
        var that = this
        options.iaClassName = "total"
        options.iaHighlight = true

        newSparkline = new Sparkline(options)
        _.map(that.rows, function(row){
            row.total = that.sumObj(row)
        })

        this.addSparkline(newSparkline, true)
        return this
    }
    ,sumObj: function(obj){
        var sum = 0
        _.each(obj, function(v, k){
            if (_.isNumber(v)) {
                sum += v
            }
        })
        return sum
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
        lineWidth: 2,
        lineColor: color('scalar'),
        fillColor: color('scalar', "light"),
        width: "100px",
        iaHighlight: false,
        iaBorderTop: false,
        iaSize: "medium",
        iaShowSparkline: true,
        iaReplaceZerosWithNulls: false,
        barColor: color("scalar")

    }
    this.userSuppliedOptions = userSuppliedOptions || {}
    this.options = {}

}
Sparkline.prototype = {
    typeSpecificDefaultOptions: function(type){
        type = type || "line"
        var defaultOptions = {
            bar:{
                iaPrimaryValue: function(values) {return _.sum(values)},
                iaSecondaryValue: function(values) {return _.max(values)},
                tooltipFormatter: function(sparkline, options, fields) {
                    console.log(fields)
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
                lineColor: color("percent"),
                fillColor: color("percent", "light"),
                iaPrimaryUnit: "%",
                iaSecondaryUnit: "%",
                chartRangeMax: 100,
                barColor: color("percent")
            },
            default: {}
        }[unit]
    }
    ,render: function(container$){
        var elem$ = ich.sparklineWithNumbers(this.options)
        container$.append(elem$)
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

        if (options.iaSize == "small") {
            options.width = "75px"
        }

        if (options.iaReplaceZerosWithNulls) {
            options.iaYvalues = _.map(options.iaYvalues, function(yValue){
                if (yValue === 0) {
                    console.log("found a zero")
                    return null
                }
                else {
                    return yValue
                }
            })
            console.log("replaced zeroes with nulls: ", options.iaYvalues)
        }

        if (options.iaHighlight) {
            options.fillColor = color(options.iaUnit, "medium") // dark color

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
    var pageController = new PagesController(location)


})