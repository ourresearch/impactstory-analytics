var Api_key_item_creates = function() {
}

Api_key_item_creates.prototype = {
    create:function(data){
        console.log("Api_key_item_creates data" , data)

        var baseOptions = {
            iaLabelWidth: "2"
        }
        var ss = new SparklineSet(data, baseOptions)

        _.each(data[0], function(val, key){
            if (typeof val === "string") return true  // continue iterating

            var iaDisplayName = key
            if (key === "9f1cf3b0290b11e281c10800200c9a66") {
                iaDisplayName = "elife's key"
            } 
            var options = {
                iaClassName: key,
                iaDisplayName: iaDisplayName,
                iaSize: "small"
            }
            ss.addSparkline(new Sparkline(options))
        })

        ss.sortBy("max").first(10).render($(".widget_api_key_item_creates"))
    }
}

