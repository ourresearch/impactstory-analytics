var Signup_funnel = function() {
}

Signup_funnel.prototype = {
    init: function(){
    }
    ,create:function(data){
        var step_names = [   
                    "any page",
                    "create page",
                    "started profile",
                    "loaded own profile"
                    ]
        var conversion_names = [   
                    "any to create",
                    "create to start profile",
                    "start to load profile"
                    ]
        var funnel_name = "omtm"
        var date_points = _.keys(data[funnel_name]).sort()
        var timestamps = _.map(date_points, function(date_string) { 
                var date = new Date(date_string); 
                return date.getTime()/1000  // return in seconds
            })
        var sorted_data = _.sortBy(data[funnel_name], function(x){return x["date"]})
        var steps_per_date = _.pluck(sorted_data, 'steps')
        var step_data  // set it up out here so can access it for the last step after the for loop

        for (step_number in _.range(step_names.length)) {
            step_data = _.map(sorted_data, function(x){ return(x["steps"][step_number]); })
            var step_data_counts = _.pluck(step_data, "count")

            // conversions aren't available on the first step
            if (step_number > 0) {
                var conversion_number = step_number - 1
                var step_data_conversions_raw = _.pluck(step_data, "step_conv_ratio")
                var step_data_conversions = _.map(step_data_conversions_raw, function(x) {
                    return Math.round(100*x) // return percentage 
                })
                var conversion_options = {
                    iaDisplayName: conversion_names[conversion_number],
                    iaPrimaryUnit: "%", 
                    iaSecondaryUnit: "%",
                    iaLabelWidth: "2",
                    chartRangeMax: 100,
                    }
                var ss_conversion = new SparklineSet($(".widget-signup_funnel"),
                    conversion_options)

                ss_conversion.createSparklineLine("signup_funnel_conversion_"+conversion_number, 
                    timestamps, 
                    step_data_conversions)
            }

            var step_options = {
                    iaDisplayName: step_names[step_number],
                    iaLabelWidth: "2",
                    }
            var ss = new SparklineSet($(".widget-signup_funnel"), 
                    step_options)

            ss.createSparklineLine("signup_funnel_step_"+step_number, 
                timestamps, 
                step_data_counts)

        }

        var step_data_counts_raw = _.pluck(step_data, "overall_conv_ratio")
        var step_data_conversions = _.map(step_data_conversions_raw, function(x) {
            return Math.round(100*x) // return percentage 
        })

        var end_to_end_options = {
                iaDisplayName: "end to end",
                iaLabelWidth: "2",
                iaPrimaryUnit: "%", 
                iaSecondaryUnit: "%",                
                }
        var ss_end_to_end = new SparklineSet($(".widget-signup_funnel"), 
                end_to_end_options)

        ss_end_to_end.createSparklineLine("signup_funnel_end_to_end", 
            timestamps, 
            step_data_counts)
    }
}

