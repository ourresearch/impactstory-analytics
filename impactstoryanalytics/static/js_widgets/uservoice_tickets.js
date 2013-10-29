function Uservoice_tickets() {
}

Uservoice_tickets.prototype = {
    create:function(data){
        var baseOptions = {
            iaLabelWidth: "1",
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment.utc(fields.x*1000).format("ddd MMM Do")
                return "<span>" + Math.round(fields.y) + '</span>' + ', ' + dateStr
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
                iaClassName: "median_open_days"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-uservoice_tickets"))
    }
}

