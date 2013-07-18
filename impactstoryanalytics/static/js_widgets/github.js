var Github = function() {
}



Github.prototype = {
    urls: {
      "webapp": "https://github.com/total-impact/total-impact-webapp/issues?state=open" ,
      "core": "https://github.com/total-impact/total-impact-core/issues?state=open"
    },
    init: function(){
    }
    ,create:function(data){
        this.createSparklineSet(data)
    }
    ,createSparklineSet: function(data){

        seriesMaxes = _.map(_.values(data), function(x) { return _.max(x) })
        max = _.max(seriesMaxes)
        console.log("using this max: ", max)

        this.createSparklineBar($("div.github-issues-webapp"), data["webapp"], max)
        this.createSparklineBar($("div.github-issues-core"), data["core"], max)
    }
    ,createSparklineBar: function(loc$, values, max, primaryNum, secondaryNum){
        if (!max) {
            var max = _.max(values)
        }
        if (!primaryNum) {
            var primaryNum = _.reduce(values, function(memo, num) { return memo + num})
        }
        if (!secondaryNum) {
            var secondaryNum = _.max(values)
        }

        console.log("setting options w this max: ", max)
        var options = {
            type:"bar",
            chartRangeMin:0,
            chartRangeMax: max,
            barWidth: 2,
            tooltipFormatter:function(sparkline, options, fields){
                console.log(fields)
                var d = new Date()
                var str = "still working on this..."
                return str
            }
        }
        loc$.find("span.primary span.value").html(primaryNum)
        loc$.find("span.secondary span.value").html(secondaryNum)
        loc$.find("span.sparkline").sparkline(values, options)

    }
}
