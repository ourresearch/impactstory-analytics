var Embedded_widget_use = function() {
}

Embedded_widget_use.prototype = {
    init: function(){
    }
    ,create:function(data){
        console.log("creating embedded_widget_use widget")

        var baseOptions = {
            iaLabelWidth: "2"
        }
        var sparklineOptions = [
            {
                iaClassName:"clickthroughs"
            },
            {
                iaClassName:"conversion-rate",
                iaYvalues: SparklineSet.conversionRate(data, "clickthroughs", "pageviews"),
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
