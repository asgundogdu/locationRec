var form=document.getElementById("form2");
    form.onsubmit = function (e) {
        e.preventDefault();
    update2()

    }

var er_data=[];    
var server = "http://35.227.40.171:8080"
var def_url2= "/cf_recommend/preprocessing=Numeric&model=SVD_implicit&dim=30&top_k=10&user=91"

var get_data = function(pval, mval, ldval, user, callback) {
    $('#loader2').show();
    if($.isEmptyObject(er_data)){

    $.getJSON(server+def_url2).then(function (data) {
                er_data = JSON.parse(JSON.stringify(data));
                callback(er_data);
            });
    }
    else {
        
        var url= '/cf_recommend/preprocessing='+pval[0]+'&model='+mval[0]+'&dim='+ldval[0]+'&top_k=10&user='+user;
        console.log(url);
            
          $.getJSON(server+url).then(function (data) {
                er_data = JSON.parse(JSON.stringify(data));
                callback(er_data);
            });  
    }   
}
    
var update2 = function() {

    var pval = $('#fpreprocessing').val();
//    console.log(pval);
    var mval = $('#fmodel').val();
//    console.log(mval);
    var ldval = $('#fld').val();
//    console.log(ldval);

//    d3.json("data/er-data.json", function(data) {
//
//            var towns = [];
//            var T = [];
//            var F = [];
//
//            data.map(function(d) {
//                    towns.push(d.town);
//                    T.push(d.T);
//                    F.push(d.F);
//                });
//
//            var trace1 = {
//              x: towns,
//              y: T,
//              name: 'True',
//              type: 'bar'
//            };
//
//            var trace2 = {
//              x: towns,
//              y: F,
//              name: 'False',
//              type: 'bar'
//            };
//
//            var data = [trace1, trace2];
//
//            var layout = {barmode: 'stack', width: d3.select(".evalchart").node().getBoundingClientRect().width, height: 265, margin: {l: 40,r: 40,b: 30,t: 10,pad: 0}, xaxis: {
//                                                title: 'Towns',
//                                                titlefont: {
//                                                  family: 'Arial, sans-serif',
//                                                  size: 10
//                                                },
//                                                showticklabels: false
//                                                    },
//                                            yaxis: {
//                                                title: 'Count',
//                                                titlefont: {
//                                                  family: 'Arial, sans-serif',
//                                                  size: 10
//                                                },
//                                                showticklabels: false
//                                                    }};
//
//            Plotly.newPlot('evalchart', data, layout);
//
//      });
//
    
    get_data1(pval, mval, ldval, user='91', function(er_data){
        console.log(er_data);
    });
    $('#loader3').hide();
}


//      d3.json('data/eda-data.geojson', function(collection) {
//
//            var users = [];
//            var noc = {};
//            collection.features.forEach(function(d, i) {
//            noc[d.properties.user_nickname] = (noc[d.properties.user_nickname] || 0) + 1;
//            });
//
//            for (var n in noc) {
//              if (noc.hasOwnProperty(n)) {
//                users.push({
//                  user: n,
//                  freq: noc[n]
//                });
//              }
//            } 
//
//          users = users.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);
//
//          d3.select('#user')
//            .attr("name", "name-list")
//            .selectAll("option")
//            .data(users).enter()
//            .append("option")
//            .text(function(d) {
//                 return d.user+": "+d.freq;
//              })
//            .attr("value", function(d) {
//                return d.user;
//                });
//
//
//
//          $('#user').on('change', function() {
//              user = this.value;
//              
//            $('#results1').remove();
//            $('#results2').remove();
//
//            $('<div id="results1"></div>').appendTo($('#map1'));
//            $('<div id="results2"></div>').appendTo($('#map2'));
//
//            var ffeatures=collection.features.filter(function(i){
//                    return ($.inArray(i.properties.user_nickname, [user]) != -1 );
//                });
//
//          var lats = [];
//          var lons = []; 
//          var towns = [];
//            ffeatures.map(function(d) {
//                    lats.push(d.properties.latitude);
//                    lons.push(d.properties.longitude);
//                    towns.push(d.properties.town);
//                });
//
//           trace = {
//                  name: user,
//                  lat: lats, 
//                  lon: lons, 
//                  text: towns,
//                  locationmode: 'USA-states', 
//                  type: 'scattergeo'
//                };
//
//                var data = [trace];
//
//                layout = {width: 400, height: 235, margin: {l: 0,r: 0,b: 0,t: 0,pad: 0},
//                  geo: {
//                    countrycolor: 'rgb(217, 217, 217)', 
//                    countrywidth: 0.5, 
//                    landcolor: 'rgb(250, 250, 250)', 
//                    projection: {type: 'albers usa'}, 
//                    scope: 'usa', 
//                    showland: true, 
//                    subunitcolor: 'rgb(217, 217, 217)', 
//                    subunitwidth: 0.5
//                  }
//                };
//                Plotly.plot('results1', {
//                  data: data,
//                  layout: layout
//                });  
//              Plotly.plot('results2', {
//                  data: data,
//                  layout: layout
//                });  
//
//              
//            var rl = ['New York','San Francisco','Boston','Atlanta','Cambridge','Chicago','Los Angeles','San Diego','Seattle','Austin']
//            
//            users = users.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);
//            
//            d3.select('#rl1')
//            .selectAll("li")
//            .data(rl.slice(0, 5)).enter()
//            .append("li")
//            .text(function(d) {
//                 return d;
//              });
//              
//            d3.select('#rl2')
//            .selectAll("li")
//            .data(rl.slice(5, 10)).enter()
//            .append("li")
//            .text(function(d) {
//                 return d;
//              });
//
//
//            });
//      });

d3.json('data/eda-data.geojson', function(collection) {
    d3.json('data/r-data.json', function(recs) {
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
              
            $('#results').remove();

            $("<div id='results' style='height: 85vh; margin-top: 10px'></div>").appendTo($('#er-m'));

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
              
        var rlats = [];
        var rlons = []; 
        var rtowns = [];
            recs.map(function(d) {
                    rlats.push(d.lat);
                    rlons.push(d.lon);
                    rtowns.push(d.location);
                });
              

           trace1 = {
                  name: "User: "+user,
                  lat: lats, 
                  lon: lons, 
                  text: towns,
                  locationmode: 'USA-states', 
                  type: 'scattergeo',
                marker: {
                    size: 8,
                    opacity: 0.6,
                    color: "#1f77b4"
                }
               
                };
            trace2 = {
                  name: "Recommendations",
                  lat: rlats, 
                  lon: rlons, 
                  text: rtowns,
                  locationmode: 'USA-states', 
                  type: 'scattergeo',
                marker: {
                    symbol: "square",
                    color: "#ff7f0e",
                    size: 8,
                    opacity: 0.8
                }
            };

                var data = [trace1, trace2];

                layout = {width: d3.select("#results").node().getBoundingClientRect().width, height: d3.select("#results").node().getBoundingClientRect().height, margin: {l: 0,r: 0,b: 0,t: 0,pad: 0},
                  geo: {
                    countrycolor: 'rgb(250, 250, 250)', 
                    countrywidth: 0.5, 
                    landcolor: 'rgb(217, 217, 217)', 
                    projection: {type: 'albers usa'}, 
                    scope: 'usa', 
                    showland: true, 
                    subunitcolor: 'rgb(250, 250, 250)', 
                    subunitwidth: 0.5
                  },
                    legend: {
                        x: 1,
                        y: 0.8
                      }
                };
              
                Plotly.plot('results', {
                  data: data,
                  layout: layout
                });   

            
            d3.select('#rl1')
            .selectAll("li")
            .data(rtowns.slice(0, 5)).enter()
            .append("li")
            .text(function(d) {
                 return "#" +String($.inArray(d, rtowns)+1) + " " + d;
              }).style("font-weight", "bold");
              
            d3.select('#rl2')
            .selectAll("li")
            .data(rtowns.slice(5, 10)).enter()
            .append("li")
            .text(function(d) {
                 return "#" +String($.inArray(d, rtowns)+1) + " " + d;
              }).style("font-weight", "bold");

                });
            });
      });