var Showstopper_papertrail_alerts = function() {
}

Showstopper_papertrail_alerts.prototype = {
    create:function(data){
        console.log("Showstopper_papertrail_alerts data" , data)
        var baseOptions = {
            iaLabelWidth: "1"
        }
        var sparklineOptions = [
            {
                iaClassName: "threw_server_error",
                iaDisplayName: "returned status=500",
                iaHref: "https://papertrailapp.com/searches/368061"
            },
            {
                iaClassName:"cant_start_thread",
                iaDisplayName: "couldn't start thread",
                iaHref: "https://papertrailapp.com/searches/137911"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })

        ss.render($(".widget-showstopper_papertrail_alerts"))
    }
}

