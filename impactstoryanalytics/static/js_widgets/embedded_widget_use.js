var Embedded_widget_use = function() {
}

Embedded_widget_use.prototype = {
    init: function(){
    }
    ,create: function(data){
        console.log("creating embedded_widget_use widget")
        console.log(data)
    }
    ,createOld:function(data){
        var overallMax = 0
        for (name in data) {
            var values =  _.pluck(data[name], "y")
            overallMax = _.max([overallMax, _.max(values)])
        }
        var ss = new SparklineSet(
            $(".widget-gmail"),
            {chartRangeMax: overallMax}
        )

        _.each(data, function(points, name) {
            var xValues = _.pluck(points, "x" )
            var yValues = _.pluck(points, "y" )
            ss.createSparklineLine(name, xValues, yValues)
        })
    }
}
