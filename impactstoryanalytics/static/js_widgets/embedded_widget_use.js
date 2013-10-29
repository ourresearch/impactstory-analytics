function Embedded_widget_use() {
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
                iaClassName: "conversion-rate",
                iaDisplayName: "conversion",
                iaYvalues: SparklineSet.conversionRate(data, "clickthroughs", "pageviews"),
                iaPrimaryValue: function(yValues) {return _.last(_.without(yValues, null))},
                iaSecondaryValue: function(yValues) {return _.max(yValues)},                
                iaUnit: "percent",
                chartRangeMax: false,
                tooltipFormatter:function(sparkline, options, fields){
                    var dateStr = moment.utc(fields.x*1000).format("MMM D")
                    return "<span>" + fields.y + '</span>%' + ', ' + dateStr
                }                
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
