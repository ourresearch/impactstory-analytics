var Github = function() {
}
Github.prototype = {
    create:function(data){
        var baseOptions = {
            type: "bar",
            iaShareYAxis: true,
            iaLabelWidth: "2"

        }
        var sparklineOptions = [
            {
                iaClassName: "webapp_issues_opened"
            },
            {
                iaClassName:"core_issues_opened"
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
