var Signup_growth = function() {
}

var convertToDailyFormat = function(data) {
    var addYValuesToTimePans = function(timepans, yValues, name){

    }


    var timestamps = data[0].x
    var timepans = []
    _.each(timestamps, function(ts, timepan_index){
        var timepan = {}
        timepan.start_iso = moment.unix(ts).format("X")
        timepan.ts = ts
        timepans.push(timepan)
    })

    _.each(data, function(lineObj){

    })



    return timepans
}


Signup_growth.prototype = {
    init: function(){
    }
    ,create:function(data){
        console.log("signup growth", data)

        for (chart_index in data) {
            var ss = new SparklineSet(
                        $(".widget-signup_growth"), 
                        {
                            iaDisplayName: data[chart_index]["display"],
                            normalRangeMin: 0,
                            normalRangeMax: 7,                            
                        })

            if (data[chart_index]["name"].indexOf("percent") >= 0) {
                var ss_percent = {iaPrimaryUnit: "%", iaSecondaryUnit: "%"}
                ss["options"] = _.extend(ss["options"], ss_percent)
            }
            ss.createSparklineLine(data[chart_index]["name"], 
                data[chart_index]["x"], 
                data[chart_index]["y"])
        }
    }
}

