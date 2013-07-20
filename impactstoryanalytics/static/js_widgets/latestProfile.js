var LatestProfile = function() {
}


LatestProfile.prototype = {
    init: function(){
    }
    ,create:function(data){
        $("iframe.latest-profile")
            .attr("src", "http://impactstory.org/" + data.url)
            .removeClass("hidden")


        var timeStr = "Created " + moment(data.date).fromNow()
        $("div.widget-latest-profile h2 span").html(timeStr)
    }
}
