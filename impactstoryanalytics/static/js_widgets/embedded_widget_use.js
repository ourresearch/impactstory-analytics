var Embedded_widget_use = function() {
}
Embedded_widget_use.prototype = {
    create:function(data){

        var baseOptions = {
            iaLabelWidth: "1"
        }
        var sparklineOptions = [
            {
                iaClassName:"pageviews"
            },
            {
                iaClassName:"conversion-rate",
                iaDisplayName: "conversion",
                iaYvalues: SparklineSet.conversionRate(data, "clickthroughs", "pageviews"),
                iaUnit: "percent",
                chartRangeMax: false
            },
            {
                iaClassName:"clickthroughs"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".embedded-widget-use"))
    }
}
