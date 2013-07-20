var Signup_funnel = function() {
}

Signup_funnel.prototype = {
    init: function(){
    }
    ,create:function(data){
        var names = [   "First page",
                        "Create page",
                        "Started profile",
                        "Loaded own profile",
                        "Returned"        
                        ]
        var funnel_name = "omtm"
        var date_points = 
        var step_data = []
        var dates = []
        
        for (date in data[funnel_name]) {
            dates.push(date)
            step_data.push([])

            for (step in data[funnel_name][date]["steps"]) {
                step_data[step].push(data[funnel_name][date]["steps"][step]["count"])
            }

            var ss = new SparklineSet(
                        $(".widget-signup_funnel signup_funnel_step_"+step), 
                        {iaDisplayName: names[step]})
            ss.createSparklineLine("signup_funnel", 
                dates, 
                step_data)

                //if (step < 4) {
                //    var ss = new SparklineSet(
                //                $(".widget-signup_funnel signup_funnel_conversion_"+step), 
                //                {   iaDisplayName: names[step], 
                //                    iaPrimaryUnit: "%", 
                //                    iaSecondaryUnit: "%"})
                //}
        }
    }
}

