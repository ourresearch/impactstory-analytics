var Signup_growth = function() {
}

Signup_growth.prototype = {
    init: function(){
    }
    ,create:function(data){
        for (chart_index in data) {
            var ss = new SparklineSet(
                        $(".widget-signup_growth"), 
                        {
                            iaDisplayName: data[chart_index]["display"],
                            normalRangeMin: 0,
                            normalRangeMax: 7,                            
                        })

            if (data[chart_index]["name"].indexOf("percent") >= 0) {
                var ss_percent = {iaPrimaryUnit: "%", iaSecondaryUnit: "%"}
                ss["options"] = _.extend(ss["options"], ss_percent)
            }
            ss.createSparklineLine(data[chart_index]["name"], 
                data[chart_index]["x"], 
                data[chart_index]["y"])
        }
    }
}

