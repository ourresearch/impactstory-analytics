var Exceptions = function() {
}

Exceptions.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment(fields.x*1000).format("ddd MMM Do")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "python"
            },
            {                
                iaClassName: "javascript",
                iaBorderTop: true                
            },
            {
                iaClassName: "conversion-rate",
                iaDisplayName: "javascript error % of pageviews",
                iaYvalues: SparklineSet.conversionRate(data, "javascript", "daily_pageviews"),
                iaUnit: "percent"
            },            
            {
                iaClassName: "daily_pageviews"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-exceptions"))
    }
}
