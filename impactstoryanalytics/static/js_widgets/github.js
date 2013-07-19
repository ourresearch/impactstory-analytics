var Github = function() {
}



Github.prototype = {
    urls: {
      "webapp": "https://github.com/total-impact/total-impact-webapp/issues?direction=asc&page=1&sort=created&state=open" ,
      "core": "https://github.com/total-impact/total-impact-core/issues?direction=asc&page=1&sort=created&state=open"
    },
    init: function(){
    }
    ,create:function(data){
        var that = this
        var seriesMaxes = _.map(_.values(data), function(x) { return _.max(x) })
        var overallMax = _.max(seriesMaxes)
        var ss = new SparklineSet(
            $(".widget-github-issues"),
            {chartRangeMax: overallMax}
        )
        _.each(data, function(values, name){
            ss.options.iaHref = that.urls[name]
            ss.createSparklineBar(name, values)

        })
    }
}
