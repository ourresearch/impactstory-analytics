function Hourly_new_users() {
}

Hourly_new_users.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment.utc(fields.x*1000).format("ddd h:mm a z")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "new_accounts",
                iaDisplayName: "new accts",
                width: "150px",
                iaLabelWidth: 2,
                iaPrimaryValue: function(values) {return _.sum(values)}
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-hourly_new_users"))
    }
}