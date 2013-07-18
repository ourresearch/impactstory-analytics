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
        seriesMaxes = _.map(_.values(data), function(x) { return _.max(x) })
        max = _.max(seriesMaxes)
        console.log("using this max: ", max)
        var isaSparkline = new IsaSparkline({chartRangeMax: max})

        isaSparkline.createSparklineBar($("div.github-issues-webapp"), data["webapp"])
        isaSparkline.createSparklineBar($("div.github-issues-core"), data["core"])
    }
}
