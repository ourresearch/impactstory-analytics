function Daily_new_users() {
}

Daily_new_users.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter:function(sparkline, options, fields){
                var dateStr = moment.utc(fields.x*1000).format("ddd MMM Do")
                return "<span>" + fields.y + '</span>' + ', ' + dateStr
            }
        }
        var sparklineOptions = [
            {
                iaClassName: "new_accounts",
                iaDisplayName: "new accts",
                //iaSize: "large",
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
        ss.render($(".widget-daily_new_users"))
    }
}