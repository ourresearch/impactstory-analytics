var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create:function(data){
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
