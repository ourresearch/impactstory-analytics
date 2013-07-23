var Daily_new_users = function() {
}

Daily_new_users.prototype = {
    init: function(){
    }
    ,create:function(data){
        for (chart_index in data) {
            var ss = new SparklineSet(
                        $(".widget-daily_new_users"), 
                        {iaDisplayName: data[chart_index]["display"]})

            if (data[chart_index]["name"].indexOf("percent") >= 0) {
                var ss_percent = {iaPrimaryUnit: "%", iaSecondaryUnit: "%"}
                ss["options"] = _.extend(ss["options"], ss_percent)
            }
            ss.createSparklineBar(data[chart_index]["name"], 
                //data[chart_index]["x"], 
                data[chart_index]["y"])
        }
    }
}

