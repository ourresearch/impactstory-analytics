function Profile_load_fail_fraction() {
}

Profile_load_fail_fraction.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment.utc(fields.x*1000).format("ddd MMM Do")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "profile_load_fail_fraction",
                iaDisplayName: "sample profile",
                iaYvalues: SparklineSet.conversionRate(data, "failed_loads", "total_loads"),
                iaUnit: "percent"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-profile_load_fail_fraction"))
    }
}