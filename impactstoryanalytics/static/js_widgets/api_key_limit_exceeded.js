function Api_key_limit_exceeded() {
}
Api_key_limit_exceeded.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                moment().zone(0)
                var dateStr = moment(fields.x*1000).format("ddd MMM Do")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "api_key_limit_exceeded",
                iaDisplayName: "Calls with key over limit"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-api_key_limit_exceeded"))
    }
}

