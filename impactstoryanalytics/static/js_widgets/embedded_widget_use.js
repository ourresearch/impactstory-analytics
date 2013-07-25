var Embedded_widget_use = function() {
}
Embedded_widget_use.prototype = {
    create:function(data){

        var baseOptions = {
            iaLabelWidth: "2"
        }
        var sparklineOptions = [
            {
                iaClassName:"clickthroughs"
            },
            {
                iaClassName:"conversion-rate", // note hyphen gets removed automatically for display name...
                iaYvalues: SparklineSet.conversionRate(data, "clickthroughs", "pageviews"),
                iaUnits: "percent" // still working on this...
            },
            {
                iaClassName:"pageviews"
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
