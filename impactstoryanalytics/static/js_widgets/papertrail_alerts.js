var Papertrail_alerts = function() {
}

Papertrail_alerts.prototype = {
    create:function(data){
        console.log("Papertrail_alerts data" , data)
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

        ss.render($(".widget-papertrail_alerts"))
    }
}

