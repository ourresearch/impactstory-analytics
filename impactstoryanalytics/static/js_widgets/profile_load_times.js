var Profile_load_times = function() {}

Profile_load_times.prototype = {
    create:function(data){
        var binWidth = data[0]["bin_end"] - data[0]["bin_start"]


        var baseOptions = {
            type: "bar",
            tooltipFormatter: function(s, o, fields){
                console.log(fields)
                var binStart = fields[0].offset * binWidth
                var binEnd = binStart + binWidth
                return "<span>"+fields[0].value+"</span>"+" loads on " +
                    binStart + "-" + binEnd + " products."

            }
        }
        var sparklineOptions = [
            {
                iaClassName: "num_load_success_null",
                iaDisplayName: "successful simple read",
                iaShareYAxis: true
            },
            {
                iaClassName:"num_load_failure_null",
                iaDisplayName: "failed simple read",
                iaShareYAxis: true
            },
            {
                iaClassName:"num_load_success_create",
                iaDisplayName: "successful after create",
                iaShareYAxis: true
            },
            {
                iaClassName:"num_load_failure_create",
                iaDisplayName: "failed after create",
                iaShareYAxis: true
            },
            {
                iaClassName:"num_load_success_refresh",
                iaDisplayName: "successful after refresh",
                iaShareYAxis: true
            },
            {
                iaClassName:"num_load_failure_refresh",
                iaDisplayName: "failed after refresh",
                iaShareYAxis: true
            }
        ]
        var ss = new SparklineSet(data, baseOptions)
        _.each(sparklineOptions, function(options){
            var sparkline = new Sparkline(options)
            ss.addSparkline(sparkline)
        })
        ss.render($(".widget-profile-load-times"))
    }
}
