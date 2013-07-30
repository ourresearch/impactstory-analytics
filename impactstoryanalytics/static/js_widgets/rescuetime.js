function Rescuetime() {
}

Rescuetime.prototype = {
    init: function(){
    }
    ,create: function(data){
        var that = this
        var div$ = $("div.widget-rescuetime")
        that.makeRickshawGraph(div$.filter(".Heather"), data.Heather)
        that.makeRickshawGraph(div$.filter(".Jason"), data.Jason)
    }
    ,makeRickshawGraph:function(div$, data){
        var graphOptions = {
            element: div$.find(".graphic")[0],
            renderer: "stack",
            width: 200,
            height: 75,
            series: [
                {
                    color: '#1A9641',
                    data: data['code'],
                    name: "Code"

                },
                {
                    color: '#D7191C',
                    data: data['email'],
                    name: "Email"
                },
                {
                    color: '#555',
                    data: data["other"],
                    name: "Other"
                }
            ]

        }
        var graph = new Rickshaw.Graph(graphOptions)

        var yAxis = new Rickshaw.Graph.Axis.Y(
            {
               graph: graph,
               orientation: 'left',
               tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
               element: div$.find("div.y_axis")[0]
            }
        );
        graph.render();

    }
    , fixDaysAgo: function(){
        // hey i can do stuff!
    }
}
