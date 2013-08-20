function Github() {
}
Github.prototype = {
    create:function(data){
        var baseOptions = {
            type: "bar",
            iaShareYAxis: true,
            iaLabelWidth: "2",
            iaPrimaryValueLabel:'',
            iaSecondaryValue: function(yValues) {return Math.round(_.last(_.without(yValues, null)))},
            iaSecondaryValueLabel: "today",            
            tooltipFormatter: function(sparkline, options, fields) {
                var number_days_ago = 30 - fields[0]["offset"]
                return fields[0]["value"] + ' issues, ' + number_days_ago + ' days ago'
            }                                               
        }
        var sparklineOptions = [
            {
                iaClassName: "webapp_issues_open"
            },
            {
                iaClassName:"core_issues_open"
            },
            {
                iaClassName:"issues_closed"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-github-issues"))
    }
}
