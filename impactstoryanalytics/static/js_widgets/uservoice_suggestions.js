var Uservoice_suggestions = function() {
}

Uservoice_suggestions.prototype = {
    init: function(){
    }
    ,create:function(data){

        for (chart_index in data) {
            var ss = new SparklineSet(
                        $(".widget-uservoice_suggestions"), 
                        {iaDisplayName: data[chart_index]["display"]})

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
