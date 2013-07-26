var Api_keys_minted = function() {
}
Api_keys_minted.prototype = {
    create:function(data){
        var baseOptions = {
            iaLabelWidth: "2"

        }
        var sparklineOptions = [
            {
                iaClassName: "cum_api_keys_minted"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-api_keys-minted"))
    }
}
