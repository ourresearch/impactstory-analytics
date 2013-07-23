var ItemsByCreatedDate = function() {
}

ItemsByCreatedDate.prototype = {
    init: function(){
    }
    ,create: function(data){
        this.createCumulativeCharts(data)
    }
    ,createDailyCharts:function(data){

    }
    ,createCumulativeCharts:function(data){

        var getYesterdayCount = function(xValues, dailyCum){
            var revDailyCum = dailyCum.slice().reverse()
            return revDailyCum[1] - revDailyCum[2]
        }

        var cumTotals = _.pluck(data, "cum_total")
        var cumProfiles = _.pluck(data, "cum_unregistered")
        var days = _.pluck(data, "date")
        var timestamps = _.map(days, function(x){
            var d = new Date(x)
            return d.getTime()
        })

        var options = {
            chartRangeMax: _.max(cumTotals),
            width: "150px",
            iaSecondaryValue: getYesterdayCount,
            iaSecondaryValueLabel: "yesterday"

        }

        var ss = new SparklineSet( $(".widget-items-by-created-date"), options)
        ss.createSparklineLine("total", timestamps, cumTotals)
        ss.createSparklineLine("profile", timestamps, cumProfiles)

    }
}
