var Gmail = function() {
}

Gmail.prototype = {
    init: function(){
    }
    ,create: function(data) {
        console.log("here's Gmail does stuff w this data, ", data)
        var graphOptions = {
            element: document.querySelector("div.widget-gmail div.graphic"),
            width: 580,
            height: 250,
            series: [
                {
                    color: 'steelblue',
                    data: data["jason"]
                },
                {
                    color: 'lightblue',
                    data: data['jason']
                }
            ]

        }


        var graph = new Rickshaw.Graph(graphOptions)

        graph.render();




    }
    , functionsLikeThis: function(){
        // hey i can do stuff!
    }
}
