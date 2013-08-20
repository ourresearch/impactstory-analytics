function Uservoice_suggestions() {
}

Uservoice_suggestions.prototype = {
    create:function(data){
        var baseOptions = {
            type: "bar",
            iaShareYAxis: true,
            iaLabelWidth: "2",
            tooltipFormatter: function(sparkline, options, fields) {
                var number_days_ago = 30 - fields[0]["offset"]
                return fields[0]["value"] + ' suggestions, ' + number_days_ago + ' days ago'
            }                                               
        }
        var sparklineOptions = [
            {
                iaClassName: "suggestions_closed",
                iaDisplayName: "closed suggestions",
                iaHref: "https://impactstory.uservoice.com/admin/forums/166950-general#/suggestions?filter=closed&sort=newest&query="
            }
        ]
        var ss = new SparklineSet(data, baseOptions)

        _.each(sparklineOptions, function(options){
            ss.addSparkline(new Sparkline(options))
        })
        ss.render($(".widget-uservoice_suggestions"))
    }
}
