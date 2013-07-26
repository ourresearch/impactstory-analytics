var Profiles_per_genre = function() {
}

Profiles_per_genre.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment(fields.x*1000).format("ddd h:mm a")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "without_response_count",
                iaDisplayName: "unanswered"
            },
            {
                iaClassName: "waiting_for_agent_count",
                iaDisplayName: "waiting for us"
            },
            {
                iaClassName: "total_count",
                iaDisplayName: "total"
            },
            {
                iaClassName: "median_open_days",
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-profiles_per_genre"))
    }
}

