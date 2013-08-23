function Profiles_per_genre() {
}

Profiles_per_genre.prototype = {
    create:function(data){
        var baseOptions = {
            iaUnit: "percent",
            iaShowSparkline: false
        }
        var sparklineOptions = [
            { iaClassName: "article",
              iaYvalues: SparklineSet.conversionRate(data, "article", "total") },
            { iaClassName: "doi",
              iaYvalues: SparklineSet.conversionRate(data, "doi", "total") },
            { iaClassName: "biblio",
              iaYvalues: SparklineSet.conversionRate(data, "biblio", "total") },
            { iaClassName: "pmid",
              iaYvalues: SparklineSet.conversionRate(data, "pmid", "total") },
            { iaClassName: "github",
              iaYvalues: SparklineSet.conversionRate(data, "github", "total") },
            { iaClassName: "figshare",
              iaYvalues: SparklineSet.conversionRate(data, "figshare", "total") },
            { iaClassName: "dryad",
              iaYvalues: SparklineSet.conversionRate(data, "dryad", "total") },
            { iaClassName: "slideshare", 
              iaYvalues: SparklineSet.conversionRate(data, "slideshare", "total") },
            { iaClassName: "url",
              iaYvalues: SparklineSet.conversionRate(data, "url", "total") },
            {
                iaClassName: "total",
                iaHighlight: true,
                iaSecondaryValue: function(){return ""},
                iaSecondaryValueLabel: "",
                iaUnit: ""
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.sortBy("max").render($(".widget-profiles_per_genre"))
    }
}

