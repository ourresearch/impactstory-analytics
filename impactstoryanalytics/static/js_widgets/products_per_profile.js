var Products_per_profile = function() {
}

Products_per_profile.prototype = {
    build_histogram_array:function(data){
        // build histogram of bin size 1
        var histogram_bin_size_1 = {}
        _.each(data, function(datapoint){
            var key = datapoint["products_per_profile"]
            var val = datapoint["number_of_profiles"]
            histogram_bin_size_1[key] = histogram_bin_size_1[key]+val || val;
        })
        _.each(_.range(Number(_.last(_.keys(histogram_bin_size_1)))), function(i){
            if (!(i in _.keys(histogram_bin_size_1))) {
                histogram_bin_size_1[i] = 0
            }
        })

        // make a sparkline of this
        var array_bin_size_1 = _.map(histogram_bin_size_1, 
                function(number_of_profiles, products_per_profile){
                                return number_of_profiles })

        return array_bin_size_1
    }

    ,build_histogram_array_binned:function(iaYvalues_bin_size_1, binSize){
        var hist_array = []
         _.each(iaYvalues_bin_size_1, 
            function(number_of_profiles, products_per_profile){
                var bin = Math.floor(products_per_profile/binSize)
                hist_array[bin] = hist_array[bin]+number_of_profiles || number_of_profiles;
            })
         return hist_array
    }    


    ,fraction: function(numerator_array, denominatorValue){
        return _.map(numerator_array, function(val){
            return Math.round(100 * val / denominatorValue)
        })
    }

    ,create:function(data){
        var that = this

        var baseOptions = {
                type: "bar",
                barWidth: 10,                
                iaPrimaryValue: function(values){return _.sum(values)},
                iaSecondaryValue: function(values) {return _.max(values)},
                iaUnit: "percent"                
            }                

        var ss = new SparklineSet(data, baseOptions)

        var iaYvalues_bin_size_1 = that.build_histogram_array(data)
        var number_of_profiles = _.sum(iaYvalues_bin_size_1)

        var options = { 
                iaClassName: "profiles_1_to_10",
                iaDisplayName: "0-10 products",
                iaYvalues: _.map(that.fraction(iaYvalues_bin_size_1, number_of_profiles).slice(1,10), Math.round),
                tooltipFormatter: function(sparkline, options, fields) {
                    var bottomBracket = fields[0]["offset"]
                    var percentofProducts = fields[0]["value"]
                    return percentofProducts+'% of profiles have '+bottomBracket+' products.'
                }                                               
        }
        var sparkline = new Sparkline(options)
        ss.addSparkline(sparkline)

        // build histogram of bin size 10
        var binned_array = that.build_histogram_array_binned(iaYvalues_bin_size_1, 10)
        var options = { 
                iaClassName: "profiles_10_to_100",
                iaDisplayName: "10-100, by 10s",
                iaYvalues: _.map(that.fraction(binned_array, number_of_profiles).slice(1,10), Math.round),
                tooltipFormatter: function(sparkline, options, fields) {
                    var stepSize = 10
                    var bottomBracket = (1+fields[0]["offset"])*stepSize
                    var upperBracket = bottomBracket + stepSize
                    var percentofProducts = fields[0]["value"]
                    return percentofProducts+'% of profiles have '+bottomBracket+'-'+upperBracket+' products.'
                }                                               
        }
        var sparkline = new Sparkline(options)
        ss.addSparkline(sparkline)

        // build histogram of bin size 100
        var binned_array = that.build_histogram_array_binned(iaYvalues_bin_size_1, 100)
        var options = { 
                iaClassName: "profiles_100_to_1000",
                iaDisplayName: "100-1000, by 100s",
                iaYvalues: _.map(that.fraction(binned_array, number_of_profiles).slice(1,10), Math.round),
                tooltipFormatter: function(sparkline, options, fields) {
                    var stepSize = 100
                    var bottomBracket = (1+fields[0]["offset"])*stepSize
                    var upperBracket = bottomBracket + stepSize
                    var percentofProducts = fields[0]["value"]
                    return percentofProducts+'% of profiles have '+bottomBracket+'-'+upperBracket+' products.'
                }                                               
        }
        var sparkline = new Sparkline(options)
        ss.addSparkline(sparkline)

        ss.render($(".widget-products_per_profile"))
    }
}
