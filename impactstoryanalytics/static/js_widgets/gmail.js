var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create:function(data){
        this.createRickshaw(data)
        this.createSparklineSet(data)
    }
    ,createSparklineSet: function(data){
        var overallMax = 0
        for (name in data) {
            var values =  _.pluck(data[name], "y")
            overallMax = _.max([overallMax, _.max(values)])
        }

        for (name in data) {
            values = _.pluck(data[name], "y")
            this.createSparkline(name, values, overallMax)
        }
    }
    ,createSparkline: function(name, values, overallMax){
        var options = {
            type:"line",
            maxSpotColor: false,
            minSpotColor: false,
            spotColor: false,
            chartRangeMax: overallMax
        }

        var loc$ = $("div.widget-gmail-sparklines ." + name)
        loc$.find("span.max-value span.value").html(_.max(values))
        loc$.find("span.current-value").html(_.last(values))
        loc$.find("span.sparkline").sparkline(values, options)

    }
    ,createRickshaw: function(data) {
        console.log("here's Gmail does stuff w this data, ", data)
        var graphOptions = {
            element: document.querySelector("div.widget-gmail div.graphic"),
            renderer: "line",
            width: 300,
            height: 150,
            series: [
                {
                    color: 'steelblue',
                    data: data["Jason"]
                },
                {
                    color: 'lightblue',
                    data: data['Heather']
                }
            ]

        }
        var graph = new Rickshaw.Graph(graphOptions)

        var xAxis = new Rickshaw.Graph.Axis.Time({
            graph: graph,
            timeUnit: (new Rickshaw.Fixtures.Time()).unit('day')
        })

        var yAxis = new Rickshaw.Graph.Axis.Y( {
                graph: graph,
                orientation: 'left',
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
                element: $("div.widget-gmail div.y_axis")[0]
            } );

        graph.render();







    }
    , functionsLikeThis: function(){
        // hey i can do stuff!
    }
}
