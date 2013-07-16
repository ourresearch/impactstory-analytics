var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create: function(data) {
        console.log("here's Gmail does stuff w this data, ", data)
        var graphOptions = {
            element: document.querySelector("div.widget-gmail div.graphic"),
            renderer: "line",
            width: 580,
            height: 250,
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
