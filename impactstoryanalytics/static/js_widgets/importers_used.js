function Importers_used() {
}

Importers_used.prototype = {
    create:function(data){
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

