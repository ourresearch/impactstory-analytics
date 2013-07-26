var Api_keys_minted = function() {
}
Api_keys_minted.prototype = {
    create:function(data){
        var baseOptions = {
            iaLabelWidth: "2",
            iaSecondaryValue: function(yValues){
                var revValues = yValues.slice().reverse()
                return revValues[1] - revValues[8]
            },
            iaSecondaryValueLabel: "last week"
        }
        var sparklineOptions = [
            {
                iaClassName: "cum_api_keys_minted",
                iaDisplayName: "API keys minted"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-api_keys-minted"))
    }
}
