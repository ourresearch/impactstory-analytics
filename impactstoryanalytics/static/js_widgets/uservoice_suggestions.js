function Uservoice_suggestions() {
}

Uservoice_suggestions.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment(fields.x*1000).format("ddd h:mm a")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "started",
            },
            {
                iaClassName: "under_review",
            },
            {
                iaClassName: "planned",
            },
            {
                iaClassName: "inbox",
                iaDisplayName: "unfiled"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-uservoice_suggestions"))
    }
}

