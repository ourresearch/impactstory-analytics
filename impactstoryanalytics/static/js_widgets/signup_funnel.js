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
        var date_points = _.keys(data[funnel_name]).sort()
        var timestamps = _.map(date_points, function(date_string) { 
                var date = new Date(date_string); 
                return date.getTime()/1000  // return in seconds
            })
        var sorted_data = _.sortBy(data["omtm"], function(x){return x["date"]})
        var steps_per_date = _.pluck(sorted_data, 'steps')

        for (step_number in _.range(names.length)) {
            var step_data = _.map(sorted_data, function(x){ return(x["steps"][step_number]); })
            var step_data_counts = _.pluck(step_data, "count")

            var ss = new SparklineSet(
                        $(".widget-signup_funnel"), 
                        {iaDisplayName: names[step_number]})

            console.log(step_number)
            console.log(date_points)
            console.log(timestamps)
            console.log(step_data_counts)

            ss.createSparklineLine("signup_funnel_step"+step_number, 
                timestamps, 
                step_data_counts)

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

