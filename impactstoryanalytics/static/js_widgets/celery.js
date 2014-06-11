function Celery() {
}

Celery.prototype = {
    create:function(data){
        var baseOptions = {
            iaLabelWidth: 2,
            iaShowSparkline: false
        }

        // var data_minimum_7_votes = _.filter(data, function(datapoint) {
        //     return datapoint.vote_count >= 7})
        console.log(data)
        var ss = new SparklineSet(data, baseOptions)

        _.each(data, function(queue){
            var options = {
                iaDisplayName: queue["queue_name"],
                iaHref: "http://impactstory-flower.herokuapp.com/tasks?limit=100",
                iaYvalues: [queue["queue_length"]],               
                iaSecondaryValue: function(yValues) {return ""},               
                iaSecondaryValueLabel: ""               
                }
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-celery"))
    }
}

