var form=document.getElementById("form2");
    form.onsubmit = function (e) {
        e.preventDefault();
    update2()

    }

var r_data=[];    
var server = "https://35.227.40.171:8080"
var def_url2= "/cf_recommend/preprocessing=Numeric&model=SVD_implicit&dim=30&top_k=10&user=91"

var get_data2 = function(pval, mval, ldval, user, callback) {
    $('#loader3').show();
    if($.isEmptyObject(r_data)){

    $.getJSON(server+def_url2).then(function (data) {
                r_data = JSON.parse(JSON.stringify(data));
                callback(r_data);
            });
    }
    else {
        
        var url= '/cf_recommend/preprocessing='+pval[0]+'&model='+mval[0]+'&dim='+ldval[0]+'&top_k=10&user='+user;
        console.log(url);
            
          $.getJSON(server+url).then(function (data) {
                r_data = JSON.parse(JSON.strinpngy(data));
                callback(r_data);
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
    
    d3.json('data/eda-data.geojson', function(collection) {

    var users = [];
    collection.features.forEach(function(d, i) {
        users.push(d.properties.user_nickname);
    });
        
    var randuser = users[Math.floor(Math.random() * users.length)];    
        $("#user").text(randuser);
    get_data2(pval, mval, ldval, user=String($.inArray(randuser, users)), function(r_data){
        
        $('#results').remove();         
        $('<div id="results" style="height: 85vh; margin-top: 10px"></div>').appendTo($('#er-m'));

                
                    var ffeatures=collection.features.filter(function(i){
                        return i.properties.user_nickname== randuser;         
                    });
        
                    var max, scale,
                      classes = 9,
                      scheme = colorbrewer["GnBu"][classes],
                      container = L.DomUtil.get('results');
                    
                      let rmap = L.map(container).setView([40, -96], 4);
                  
                  var osmtiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
                  });
                    
                    rmap.addLayer(osmtiles);

//    d3.json('data/r-data.json', function(r_data) {
        
                    var recs = r_data.slice(0,10);
                    var rlats = [];
                    var rlons = []; 
                    var rtowns = [];
                        recs.map(function(d) {
                                rlats.push(d.lat);
                                rlons.push(d.lon);
                                rtowns.push(d.Recommendations);
                            }); 
//                    console.log(rtowns, rlats, rlons);
                        
                    var acts = r_data.slice(10,r_data.length);    
                    var alats = [];
                    var alons = []; 
                    var atowns = [];
                        acts.map(function(d) {
                                alats.push(d.lat);
                                alons.push(d.lon);
                                atowns.push(d.Actuals);
                            });
//                    console.log(atowns, alats, alons); 
                        
                    var rIcon = L.icon({
                        iconUrl: 'images/r.png',
                        iconSize: [20,30]
                      });
                        
                    var aIcon = L.icon({
                        iconUrl: 'images/a.png',
                        iconSize: [20,30]
                      });
                        
                    for(var r=0; r < recs.length; r++)  {
//                        console.log([rlats[r], rlons[r]]); 
                        let marker = L.marker([rlats[r], rlons[r]],{icon: rIcon})
                        .bindPopup(rtowns[r])
//                        .on('mouseover', function (e) {
//                            this.openPopup();
//                            })
//                        .on('mouseout', function (e) {
//                                this.closePopup();
//                            })
                        .addTo(rmap);
                    }
                        
                    for(var a=0; a < acts.length; a++)  {
//                        console.log([alats[a], alons[a]]); 
                        let marker = L.marker([alats[a], alons[a]],{icon: aIcon})
                        .bindPopup(atowns[a])
//                        .on('mouseover', function (e) {
//                            this.openPopup();
//                            })
//                        .on('mouseout', function (e) {
//                                this.closePopup();
//                            })
                        .addTo(rmap);
                    }  
                        
                    $('#loader3').hide();
                     
        d3.select("#rlegend").selectAll("svg").remove();
        var svg = d3.select("#rlegend")
                   .append("svg")
                   .attr("height", d3.select("#rlegend").node().getBoundingClientRect().height)
                   .attr("width", d3.select("#rlegend").node().getBoundingClientRect().width);

                    svg.append("svg:image")
                        .attr('x', 8)
                        .attr('y', 15)
                        .attr('width', 40)
                        .attr('height', 30)
                        .attr("xlink:href", 'images/a.png')
        
                    svg.append("svg:image")
                        .attr('x', 8)
                        .attr('y', 48)
                        .attr('width', 40)
                        .attr('height', 30)
                        .attr("xlink:href", 'images/r.png')
        
                    svg.append("text")
                        .attr('x', 48)
                        .attr('y', 33)
                        .text('- Visited')
                        .style("font-weight", "bold");
        
                    svg.append("text")
                        .attr('x', 48)
                        .attr('y', 63)
                        .text('- Recommendation')
                        .style("font-weight", "bold");
        
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
// }); 
    });    
    });
            
       
}






   
            


