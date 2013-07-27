var Importers_used = function() {
}

Importers_used.prototype = {
    create:function(data){
        console.log("Importers_used data" , data)
        var baseOptions = {
            iaUnit: "percent",
            iaLabelWidth: "1"
        }
        var sparklineOptions = [
            {
                iaClassName: "orcid_perc",
                iaDisplayName: "%ORCID"
            },
            {
                iaClassName:"bibtex_perc",
                iaDisplayName: "%BibTex"
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-importers-used"))
    }
}

