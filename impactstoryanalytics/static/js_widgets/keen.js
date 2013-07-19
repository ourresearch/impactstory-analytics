var Keen = function() {
}

Keen.prototype = {
    init: function(){
    }
    ,create:function(data){
        for (chart_index in data) {
            var ss_absolute = new SparklineSet(
                        $(".widget-keen"), 
                        { 
                            iaDisplayName: data[chart_index]["display"]
                        })
            var ss_percent = new SparklineSet(
                        $(".widget-keen"),
                        {   
                            iaDisplayName: data[chart_index]["display"],
                            iaPrimaryUnit: "%",   
                            iaSecondaryUnit: "%"   
                        })

            var ss = ss_absolute
            if (data[chart_index]["name"].indexOf("percent") >= 0) {
                ss = ss_percent
            }
            ss.createSparklineLine(data[chart_index]["name"], 
                data[chart_index]["x"], 
                data[chart_index]["y"])
        }
    }
}

