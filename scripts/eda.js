(function () {
              var max, scale,
                  classes = 9,
                  scheme = colorbrewer["GnBu"][classes],
                  container = L.DomUtil.get('hex'),
                  map = L.map(container).setView([40, -96], 4);

              var osmtiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                  attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
              });
              map.addLayer(osmtiles);

              d3.json(container.dataset.source, function(collection) {
                  
                var hexlay = L.hexLayer(collection, {
                      applyStyle: hex_style
                });
                  
                map.addLayer(hexlay);
                  
                var datedata = [];
                var noc = {};
                collection.features.forEach(function(d, i) {
                noc[d.properties.date] = (noc[d.properties.date] || 0) + 1;
                });

                var parseDate = d3.time.format("%b %Y").parse;
                  
                for (var n in noc) {
                  if (noc.hasOwnProperty(n)) {
                    datedata.push({
                      date: parseDate(n),
                      freq: noc[n]
                    });
                  }
                } 
                  
                var citydata = [];
                var noc = {};
                collection.features.forEach(function(d, i) {
                noc[d.properties.town] = (noc[d.properties.town] || 0) + 1;
                });
                  
                for (var n in noc) {
                  if (noc.hasOwnProperty(n)) {
                    citydata.push({
                      town: n,
                      freq: noc[n]
                    });
                  }
                } 
                  
                citydata = citydata.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);
                  
                var width = d3.select(".datechart").node().getBoundingClientRect().width;
                  
//            Date Chart 
                  
                var dateheight = 100
                var x = d3.time.scale().range([0, width-10]),
                    y = d3.scale.linear().range([dateheight, 0]);
  
                var xAxis = d3.svg.axis().scale(x).orient("bottom");

                var brush = d3.svg.brush()
                      .x(x)
                      .on("brush", brushed);

                var area = d3.svg.area()
                      .interpolate("monotone")
                      .x(function (d) { return x(d.date); })
                      .y0(dateheight)
                      .y1(function (d) { return y(d.freq); });

                var svg = d3.select(".datechart").append("svg")
                      .attr("width", width)
                      .attr("height", dateheight + 18.8);

                var Date = svg.append("g")
                      .attr("class", "Date").attr("transform", "translate(11.5, 0)");  
                
                x.domain(d3.extent(datedata.map(function (d) { return d.date; })));
                y.domain([0, d3.max(datedata.map(function (d) { return d.freq; }))]);
                  
                Date.append("path")
                    .datum(datedata)
                    .attr("class", "area")
                    .attr("d", area);
                  
                Date.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0,100)")
                    .call(xAxis);

                Date.append("g")
                    .attr("class", "x brush")
                    .call(brush)
                  .selectAll("rect")
                    .attr("height", dateheight);
                  

                function brushed() {
                    var s = brush.extent();
                    var ffeatures=collection.features.filter(function(i){
                        return parseDate(i.properties.date)>=s[0]&& parseDate(i.properties.date)<= s[1];         
                    });

                    var ucitydata = [];
                    var noc = {};
                    ffeatures.forEach(function(d, i) {
                    noc[d.properties.town] = (noc[d.properties.town] || 0) + 1;
                    });

                    for (var n in noc) {
                      if (noc.hasOwnProperty(n)) {
                        ucitydata.push({
                          town: n,
                          freq: noc[n]
                        });
                      }
                    } 
                    ucitydata = ucitydata.sort((a, b) => parseFloat(b.freq) - parseFloat(a.freq)).slice(0, 10);
                    
                    citydata = brush.empty() ? citydata : ucitydata;
                    
                    d3.select(".citychart").selectAll(".bar").remove();
                    d3.select(".citychart").selectAll(".y.axis").remove();
                    
                    y.domain(citydata.map(function(d) {
                      return d.town;
                    }));
                    x.domain([0, d3.max(citydata, function(d) {
                      return d.freq;
                    })]);
                    
                    var svg = d3.select(".citychart").append("svg")
                        .attr("width", width)
                        .attr("height", cityheight)
                        .append("g")
                        .attr("transform", "translate(65, 0)");

                    var citychart = svg.selectAll(".bar")
                        .data(citydata)
                        .enter()
                        .append("g");

                    citychart.append("g")
                      .attr("class", "y axis")
                      .call(yAxis).append("text");

                    citychart.append("rect")
                        .attr("class", "bar")
                        .attr("y", function (d) {
                            return y(d.town);
                        })
                        .attr("height", y.rangeBand())
                        .attr("x", 0)
                        .attr("width", function (d) {
                            return x(d.freq);
                        });     

                    citychart.append("text")
                        .attr("class", "label")
                        .attr("y", function (d) {
                            return y(d.town) + y.rangeBand() / 2 + 4;
                        })
                        .attr("x", function (d) {
                            return x(d.freq) - 15;
                        })
                        .text(function (d) {
                            return d.freq;
                        })
                        .style("fill", "white");
                    
                    map.getContainer().remove();
//                    console.log(old)
                    $('<div id="hex" data-source="data/eda-data.geojson" style="height: 85vh; margin-top: 10px"></div>').appendTo($('#eda-m'));

                    var max, scale,
                      classes = 9,
                      scheme = colorbrewer["GnBu"][classes],
                      container = L.DomUtil.get('hex');
                    
                      map = L.map(container).setView([40, -96], 4);

                  var osmtiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
                  });
                  map.addLayer(osmtiles);
                    
                d3.json('data/eda-data.geojson', function(fcollection) {
//                  
                    hexlay = L.hexLayer(fcollection, {
                          applyStyle: hex_style
                    });
//
                    map.addLayer(hexlay);
                    });
                  }

              function type(d) {
                d.freq = +d.freq;
                return d;
              }  
                  
//            Top 10 City Chart  
            var cityheight = 200;
            var y = d3.scale.ordinal()
                .rangeRoundBands([cityheight, 0], .1);

            var x = d3.scale.linear()
                .range([0, width-65]);
                  
            var yAxis = d3.svg.axis()
                .scale(y).tickSize(0)
                .orient("left");
                  
            var svg = d3.select(".citychart").append("svg")
                .attr("width", width)
                .attr("height", cityheight)
                .append("g")
                .attr("transform", "translate(65, 0)");
                  
            var citychart = svg.selectAll(".bar")
                .data(citydata)
                .enter()
                .append("g");
                  
            y.domain(citydata.map(function(d) {
              return d.town;
            }));
            x.domain([0, d3.max(citydata, function(d) {
              return d.freq;
            })]);

            citychart.append("g")
              .attr("class", "y axis")
              .call(yAxis).append("text");

            citychart.append("rect")
                .attr("class", "bar")
                .attr("y", function (d) {
                    return y(d.town);
                })
                .attr("height", y.rangeBand())
                .attr("x", 0)
                .attr("width", function (d) {
                    return x(d.freq);
                });     
                   
              citychart.append("text")
                .attr("class", "label")
                .attr("y", function (d) {
                    return y(d.town) + y.rangeBand() / 2 + 4;
                })
                .attr("x", function (d) {
                    return x(d.freq) - 15;
                })
                .text(function (d) {
                    return d.freq;
                })
                .style("fill", "white");
                  
              });
  
              function hex_style(hexagons) {
                  if (!(max && scale)) {
                      max = d3.max(hexagons.data(), function (d) { return d.length; });
                      scale = d3.scale.quantize()
                              .domain([0, max])
                              .range(d3.range(classes));
                  }

                  hexagons
                      .attr("stroke", scheme[classes - 1])
                      .attr("fill", function (d) {
                          return scheme[scale(d.length)];
                      });
              }
          }());