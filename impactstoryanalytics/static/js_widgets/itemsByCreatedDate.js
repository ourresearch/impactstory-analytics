var ItemsByCreatedDate = function() {
}

ItemsByCreatedDate.prototype = {
    init: function(){
    }
    ,create: function(data){
        console.log("raw data: ", data)
        var baseOptions = {
            type: "line",
            iaShareYAxis: true,
            width: "125px",
            iaSecondaryValue: function(yValues){
                var revValues = yValues.slice().reverse()
                return revValues[1] - revValues[2]
            },
            iaSecondaryValueLabel: "yesterday"
        }
        var sparklineOptions = [
            {
                iaClassName: "cum_total",
                iaDisplayName: "total"
            },
            {
                iaClassName:"cum_registered",
                iaDisplayName: "registered"
            },
            {
                iaClassName:"cum_unregistered",
                iaDisplayName: "unregistered"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-items-by-created-date"))
    }
}
