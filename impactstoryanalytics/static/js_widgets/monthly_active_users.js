function Monthly_active_users() {
}

Monthly_active_users.prototype = {
    init: function(){
    }
    ,create:function(data){
        var baseOptions = {
            iaLabelWidth: "2"
        }
        var sparklineOptions = [
            {
                iaClassName: "accounts"
            },
            {
                iaClassName:"percent_MAU",
                iaUnit: "percent",
                chartRangeMax: false
            },
            {
                iaClassName:"monthly_actives"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-monthly_active_users"))
    }
}

