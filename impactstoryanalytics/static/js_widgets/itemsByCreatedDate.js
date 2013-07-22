var ItemsByCreatedDate = function() {
}

ItemsByCreatedDate.prototype = {
    init: function(){
    }
    ,create:function(data){
        var that = this

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
            iaLabelWidth: "2",
            iaSecondaryValue: function(xValues, yValues){ return "hi!"}

        }

        var ss = new SparklineSet( $(".widget-items-by-created-date"), options)
        ss.createSparklineLine("total", timestamps, cumTotals)
        ss.createSparklineLine("profile", timestamps, cumProfiles)

    }
}
