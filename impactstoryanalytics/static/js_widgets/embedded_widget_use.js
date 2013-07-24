var Embedded_widget_use = function() {
}

Embedded_widget_use.prototype = {
    init: function(){
    }
    ,create:function(data){
        console.log("creating embedded_widget_use widget")
        console.log(data)
        var overallMax = this.findOverallMax(data)

        var ss = new SparklineSet(
            $(".embedded-widget-use"),
            {chartRangeMax: overallMax}
        )
        var xValues = _.map(_.pluck(data, "start_iso"), function(iso){
            return moment(iso).format("X")
        })

        var conversionRate = _.map(data, function(row){
            if (!row.pageviews) {
                return null
            }
            else {
                return Math.round(100 * row.clickthroughs / row.pageviews)
            }
        })
        console.log("conversion rate", conversionRate)


        ss.createSparklineLine("clickthroughs", xValues, _.pluck(data, "clickthroughs"))
        ss.createSparklineLine("pageviews", xValues, _.pluck(data, "pageviews"))
        ss.options.iaPrimaryUnit = "%"
        ss.createSparklineLine("conversion-rate", xValues, conversionRate)

    }
    ,findOverallMax: function(data){
        var overallMax = 0
        for (var timeslice in data) {
            var thisTimeSliceMax = _.max([timeslice.clickthroughs, timeslice.pageviews])
            overallMax = _.max([overallMax, thisTimeSliceMax])
        }
        return overallMax
    }
}
