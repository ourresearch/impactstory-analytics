function Signup_growth() {
}

Signup_growth.prototype = {
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
                iaClassName:"percent_growth",
                iaUnit: "percent",
                chartRangeMax: false
            },
            {
                iaClassName:"new_accounts_per_week",
                iaDisplayName:"new accounts/wk"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-signup_growth"))
    }
}

