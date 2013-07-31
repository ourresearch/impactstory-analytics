function Provider_errors() {
}

Provider_errors.prototype = {
    create:function(data){
        console.log("Provider_errors data" , data)
        var baseOptions = {
            iaLabelWidth: "2"
        }

        var sparklineOptions = [
            {
                iaClassName: "provider_request_exception",
                iaDisplayName: "RequestException",
                iaHref: "https://papertrailapp.com/groups/74491/events?q=RequestException"
            },
            {
                iaClassName:"provider_timeout",
                iaDisplayName: "timeout",
                iaHref: "https://papertrailapp.com/groups/74491/events?q=%22Provider+timed+out+during+GET+on%22"
            },
            {
                iaClassName:"provider_error_response",
                iaDisplayName: "status 4xx or 5xx",
                iaHref: "https://papertrailapp.com/groups/74491/events?q=ProviderServerError+OR+ProviderClientError"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })

        ss.render($(".widget-provider_errors"))
    }
}

