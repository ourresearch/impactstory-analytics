var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create:function(data){
        this.createSparklineSet(data)
    }
    ,createSparklineSet: function(data){
        var that = this
        var overallMax = 0
        for (name in data) {
            var values =  _.pluck(data[name], "y")
            overallMax = _.max([overallMax, _.max(values)])
        }

        _.each(data, function(points, name) {
            var xValues = _.pluck(points, "x" )
            var yValues = _.pluck(points, "y" )
            that.createSparkline(name, xValues, yValues, overallMax)
        })
    }
    ,createSparkline: function(name, xValues, yValues, overallMax){
        var weekDays = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        var options = {
            type:"line",
            maxSpotColor: false,
            minSpotColor: false,
            spotColor: false,
            chartRangeMin:0,
            tooltipFormatter:function(sparkline, options, fields){
                var d = new Date(fields.x * 1000)
                var mins = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes()
                var dateStr = weekDays[d.getDay()] + ' ' + d.getHours() + ':' + mins
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        options.chartRangeMax = overallMax
        options.xvalues = xValues

        var loc$ = $("div.widget-gmail-sparklines ." + name)
        loc$.find("span.max-value span.value").html(_.max(yValues))
        loc$.find("span.current-value").html(_.last(yValues))
        loc$.find("span.sparkline").sparkline(yValues, options)

    }
    , functionsLikeThis: function(){
        // hey i can do stuff!
    }
}
