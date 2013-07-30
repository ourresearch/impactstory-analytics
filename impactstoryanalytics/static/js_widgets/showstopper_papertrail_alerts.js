var Showstopper_papertrail_alerts = function() {
}

Showstopper_papertrail_alerts.prototype = {
    create:function(data){
        console.log("Showstopper_papertrail_alerts data" , data)
        var baseOptions = {
            iaLabelWidth: "1"
        }
        var ss = new SparklineSet(data, baseOptions)

        _.each(data[0], function(val, key){
            if (typeof val === "string") return true  // continue iterating

            var options = {
                iaClassName: key
            }
            ss.addSparkline(new Sparkline(options))
        })

        ss.render($(".widget-showstopper_papertrail_alerts"))
    }
}

