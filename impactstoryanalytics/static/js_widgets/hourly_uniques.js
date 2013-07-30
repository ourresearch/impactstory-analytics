var Hourly_uniques = function() {
}

Hourly_uniques.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                moment().zone(0)
                var dateStr = moment.utc(fields.x*1000).format("ddd h:mm a z")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName:"hourly_uniques",
                iaLabelWidth: "2"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-hourly_uniques"))
    }
}
