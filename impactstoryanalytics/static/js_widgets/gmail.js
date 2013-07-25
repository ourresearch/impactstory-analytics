var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create:function(data){
        var baseOptions = {}
        var sparklineOptions = [
            {
                iaClassName: "Jason",
                iaShareYAxis: true
            },
            {
                iaClassName:"Heather",
                iaShareYAxis: true
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-gmail"))
    }
}
