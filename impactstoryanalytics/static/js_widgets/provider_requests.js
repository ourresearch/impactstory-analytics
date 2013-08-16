function Provider_requests() {
}

Provider_requests.prototype = {
    create:function(data){
        console.log("Provider_requests data" , data)
        var baseOptions = {
            iaLabelWidth: "1"
        }
        var ss = new SparklineSet(data, baseOptions)

        _.each(data[0], function(val, key){
            if (typeof val === "string") return true  // continue iterating

            var options = {
                iaClassName: key,
                iaSize: "small"
            }
            ss.addSparkline(new Sparkline(options))
        })

        ss.sortBy("last").render($(".widget-provider-requests"))
    }
}

