function Uservoice_suggestions_upvoted() {
}

Uservoice_suggestions_upvoted.prototype = {
    create:function(data){
        var baseOptions = {
            iaLabelWidth: 2,
            iaShowSparkline: false
        }

        var data_minimum_7_votes = _.filter(data, function(datapoint) {
            return datapoint.vote_count >= 7})
        var ss = new SparklineSet(data_minimum_7_votes, baseOptions)
        _.each(data_minimum_7_votes.slice(0,5), function(suggestion){
            var options = {
                    iaDisplayName: suggestion["title"],
                    iaHref: suggestion["url"],
                    iaYvalues: [suggestion["vote_count"]],               
                    iaSecondaryValue: function(yValues) {return suggestion["subscriber_count"]},               
                    iaSecondaryValueLabel: "subscribers"               
                }
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-uservoice_suggestions_upvoted"))
    }
}

