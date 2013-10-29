function Signup_funnel() {
}

Signup_funnel.prototype = {
    init: function(){
    }
    ,create:function(data){
        var baseOptions = {
            iaLabelWidth: "2"

        }
        var sparklineOptions = [
            {
                iaClassName: "0_count",
                iaDisplayName: "visited any page"
            },
            {
                iaClassName:"1_conv",
                iaUnit: "percent",
                chartRangeMax: false,                
                iaDisplayName: " "

            },
            {
                iaClassName: "1_count",
                iaDisplayName: "visited create page",
                iaBorderTop: true

            },
            {
                iaClassName:"2_conv",
                iaUnit: "percent",
                chartRangeMax: false,                
                iaDisplayName: " "

            },
            {
                iaClassName: "2_count",
                iaDisplayName: "started profile",
                iaBorderTop: true

            },
            {
                iaClassName:"3_conv",
                iaUnit: "percent",
                chartRangeMax: false,                
                iaDisplayName: " "

            },
            {
                iaClassName: "3_count",
                iaDisplayName: "made profile",
                iaBorderTop: true

            },
            {
                iaClassName: "signup_conv",
                iaDisplayName: "end-to-end",
                iaUnit: "percent",
                chartRangeMax: false,
                iaHighlight: true

            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-signup_funnel"))
        }
}

