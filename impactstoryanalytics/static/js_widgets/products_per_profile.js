var Products_per_profile = function() {
}

Products_per_profile.prototype = {
    create:function(data){
        var baseOptions = {
            tooltipFormatter: function(sparkline, options, fields){
                console.log("fields in products_per_profile tooltip:")
                console.log(fields)
                //var dateStr = moment(fields.x*1000).format("ddd h:mm a")
                //return "<span>" + fields.y + '</span>' + ', ' + dateStr
                return "<span>hi</span>"
            }
        }

        var options = { 
                iaClassName: "histogram"
            }
        var ss = new SparklineSet(data, baseOptions)
        var sparkline = new Sparkline(options)
        ss.addSparkline(sparkline)
        ss.render($(".widget-products_per_profile"))
    }
}

