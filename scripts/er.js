var form=document.getElementById("form2");
    form.onsubmit = function (e) {
        e.preventDefault();
    update2()

    }

var update2 = function() {

    var pval = $('#fpreprocessing').val();
//    console.log(pval);
    var mval = $('#fmodel').val();
//    console.log(mval);
    var ldval = $('#fld').val();
//    console.log(ldval);

    d3.json("data/er-data.json", function(data) {

            var towns = [];
            var T = [];
            var F = [];

            data.map(function(d) {
                    towns.push(d.town);
                    T.push(d.T);
                    F.push(d.F);
                });

            var trace1 = {
              x: towns,
              y: T,
              name: 'True',
              type: 'bar'
            };

            var trace2 = {
              x: towns,
              y: F,
              name: 'False',
              type: 'bar'
            };

            var data = [trace1, trace2];

            var layout = {barmode: 'stack', width: d3.select(".evalchart").node().getBoundingClientRect().width, height: 265, margin: {l: 40,r: 40,b: 30,t: 10,pad: 0}, xaxis: {
                                                title: 'Towns',
                                                titlefont: {
                                                  family: 'Arial, sans-serif',
                                                  size: 10
                                                },
                                                showticklabels: false
                                                    },
                                            yaxis: {
                                                title: 'Count',
                                                titlefont: {
                                                  family: 'Arial, sans-serif',
                                                  size: 10
                                                },
                                                showticklabels: false
                                                    }};

            Plotly.newPlot('evalchart', data, layout);

      });

}

      d3.json('data/eda-data.geojson', function(collection) {

            var users = [];
            var noc = {};
            collection.features.forEach(function(d, i) {
            noc[d.properties.user_nickname] = (noc[d.properties.user_nickname] || 0) + 1;
            });

            for (var n in noc) {
              if (noc.hasOwnProperty(n)) {
                users.push({
                  user: n,
                  freq: noc[n]
                });
              }
            } 

          users = users.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);

          d3.select('#user')
            .attr("name", "name-list")
            .selectAll("option")
            .data(users).enter()
            .append("option")
            .text(function(d) {
                 return d.user+": "+d.freq;
              })
            .attr("value", function(d) {
                return d.user;
                });



          $('#user').on('change', function() {
              user = this.value;
              
            $('#results1').remove();
            $('#results2').remove();

            $('<div id="results1"></div>').appendTo($('#map1'));
            $('<div id="results2"></div>').appendTo($('#map2'));

            var ffeatures=collection.features.filter(function(i){
                    return ($.inArray(i.properties.user_nickname, [user]) != -1 );
                });

          var lats = [];
          var lons = []; 
          var towns = [];
            ffeatures.map(function(d) {
                    lats.push(d.properties.latitude);
                    lons.push(d.properties.longitude);
                    towns.push(d.properties.town);
                });

           trace = {
                  name: user,
                  lat: lats, 
                  lon: lons, 
                  text: towns,
                  locationmode: 'USA-states', 
                  type: 'scattergeo'
                };

                var data = [trace];

                layout = {width: 400, height: 235, margin: {l: 0,r: 0,b: 0,t: 0,pad: 0},
                  geo: {
                    countrycolor: 'rgb(217, 217, 217)', 
                    countrywidth: 0.5, 
                    landcolor: 'rgb(250, 250, 250)', 
                    projection: {type: 'albers usa'}, 
                    scope: 'usa', 
                    showland: true, 
                    subunitcolor: 'rgb(217, 217, 217)', 
                    subunitwidth: 0.5
                  }
                };
                Plotly.plot('results1', {
                  data: data,
                  layout: layout
                });  
              Plotly.plot('results2', {
                  data: data,
                  layout: layout
                });  
              
            var rl = ['tnjrs','tnjrs','tnjrs','tnjrs','tnjrs','tn','tn','tn','tn','tn']
            
            users = users.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);
            
            d3.select('#rl1')
            .selectAll("li")
            .data(rl.slice(0, 5)).enter()
            .append("li").transition().delay(600)
            .text(function(d) {
                 return d;
              });
              
            d3.select('#rl2')
            .selectAll("li")
            .data(rl.slice(5, 10)).enter()
            .append("li").transition().delay(600)
            .text(function(d) {
                 return d;
              });


            });
      });