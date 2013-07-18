var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create:function(data){
        this.createSparklineSet(data)
    }
    ,createSparklineSet: function(data){
        var that = this
        var overallMax = 0
        for (name in data) {
            var values =  _.pluck(data[name], "y")
            overallMax = _.max([overallMax, _.max(values)])
        }
        var isaSparkline = new IsaSparkline({chartRangeMax: overallMax})

        _.each(data, function(points, name) {
            var xValues = _.pluck(points, "x" )
            var yValues = _.pluck(points, "y" )
            var loc$ = $("div.widget-gmail-sparklines."+name)
            isaSparkline.createSparklineLine(loc$, xValues, yValues)
        })
    }
}
