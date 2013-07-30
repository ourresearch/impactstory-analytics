var Provider_errors = function() {
}

Provider_errors.prototype = {
    create:function(data){
        console.log("Provider_errors data" , data)
        var baseOptions = {
            iaLabelWidth: "2"
        }
        var ss = new SparklineSet(data, baseOptions)

        displayNames = {
            "provider_request_exception": "RequestException",
            "provider_error_response": "other response error",
            "provider_timeout": "timeout",
            }

        _.each(data[0], function(val, key){
            if (typeof val === "string") return true  // continue iterating

            var options = {
                iaClassName: key,
                iaDisplayName: displayNames[key]
            }
            ss.addSparkline(new Sparkline(options))
        })

        ss.render($(".widget-provider_errors"))
    }
}

