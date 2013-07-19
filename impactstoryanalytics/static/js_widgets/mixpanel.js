var Mixpanel = function() {
}

Mixpanel.prototype = {
    init: function(){
    }
    ,create:function(data){
        var overallMax = 0
        for (name in data) {
            var values =  data[name]["y"]
            overallMax = _.max([overallMax, _.max(values)])
        }

        var ss = new SparklineSet(
                    $(".widget-mixpanel"),
                    {   chartRangeMax: overallMax, 
                        iaPrimaryUnit: "%",   
                        iaSecondaryUnit: "%"   
                    })

        for (name in data) {
            var xValues =  data[name]["x"]
            var yValues =  data[name]["y"]
            ss.createSparklineLine(name, xValues, yValues)
        }
    }
}

