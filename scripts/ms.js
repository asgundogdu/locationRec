        var form=document.getElementById("form1");
            form.onsubmit = function (e) {
                e.preventDefault();
            update()

            }
    var update = function() {

    var pvals = $('#preprocessing').val();
    console.log(pvals);
    var mvals = $('#model').val();
    console.log(mvals);
    var ldvals = $('#ld').val();
//    console.log(ldvals);
    var mtval = $('#metric').val();
    console.log(mtval);

    d3.json("data/ht-data.json", function (data) {
        var m;
        for(m=0; m<mvals.length;m++){
            d3.select(".htchart"+String(m+1)).selectAll("path").remove();
            d3.select(".htchart"+String(m+1)).selectAll("text").remove();
            d3.select(".htchart"+String(m+1)).selectAll("rect").remove();
            
            var mdata=data.filter(function(i){
                            return i.Model==mvals[m];         
                        });

            var margin = {top: 20, right: 20, bottom: 40, left: 40},
                width = d3.select(".htchart1").node().getBoundingClientRect().width - margin.left - margin.right,
                height = d3.select(".htchart1").node().getBoundingClientRect().height - margin.top - margin.bottom;

            var x = d3.scale.linear().range([0, width]);
            var y = d3.scale.linear().range([height, 0]);

            var xAxis = d3.svg.axis().scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis().scale(y)
                .orient("left");

            var line = d3.select(".htchart"+String(m+1))
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform", 
                          "translate(" + margin.left + "," + margin.top + ")");
            var valueline = d3.svg.line()
                .interpolate("basis")
                .x(function(d) {return x(d.x); })
                .y(function(d) { return y(d.y); });

            x.domain([0, 100]);
            y.domain([0, 1]); 
            
            var domain=[];
            
            var l;
            for(l=0; l<pvals.length;l++){

                var ldata=mdata.filter(function(i){
                            return i.Preprocessing==pvals[l];         
                        });
                var color = ["red", "steelblue"];

                var ldata = ldata.map(function(d) {
                return {
                    x: d.LatentDimensions,
                    y: d[mtval[0]]
                };
                });
                
                
                domain.push("Preprocessing: "+pvals[l]);

                line.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis)
                   .append("text")            
                    .attr("x", width / 2)
                    .attr("y", 30 )
                    .style("text-anchor", "middle")
                    .text("Latent Dimensions");

                line.append("g")
                    .attr("class", "y axis")
                    .call(yAxis)
                   .append("text")            
                    .attr("transform", "rotate(-90)")
                    .attr("y", -30 )
                    .attr("x", 0 - height/2 )             
                    .style("text-anchor", "middle")
                    .text(mtval[0]);

                line.append("text")
                    .attr("x", (width / 2))             
                    .attr("y", 0)
                    .attr("text-anchor", "middle")  
                    .style("font-size", "10px")
                    .text("Model: "+mvals[m]);

                line.append("path")
                    .style("stroke", color[l])
                    .style("stroke-width", "3")
                    .style("fill", "none")
                    .attr("class", "line")
                    .attr("d", valueline(ldata));
            }
            
                var lcolor = d3.scale.ordinal()
                    .domain(domain)
                    .range(["red", "steelblue"]);
            
                var legend = line.selectAll(".legend")
                      .data(lcolor.domain())
                    .enter().append("g")
                      .attr("class", "legend")
                      .attr("transform", function(d, i) { return "translate(0," + i * 15 + ")"; });

                    legend.append("rect")
                      .attr("x", width - 73)
                      .attr("y", 34)  
                      .attr("width", 10)
                      .attr("height", 10)
                      .style("fill", lcolor);

                    legend.append("text")
                      .attr("x", width - 60)
                      .attr("y", 34)
                      .attr("dy", ".60em")
                        .style("font-size", 14)
                      .text(function(d) { return d; });
        }
        
        var vpdata=data.filter(function(i){
                            return ($.inArray(i.Model, mvals) != -1 && $.inArray(String(i.Preprocessing), pvals) != -1);         
                        });
        
        var tdata = [];
        
        for(m=0; m<mvals.length;m++){
            
            var mdata=vpdata.filter(function(i){
                            return i.Model==mvals[m];         
                        });
            var t = [];
            mdata.map(function(d) {
                    t.push(d[mtval[0]]);
                });
 
            console.log(t);
        
            var trace = {
              y: t,
              type: 'violin'
            };
            
            tdata.push(trace);
        }

        Plotly.newPlot('mschart', tdata);
        
    
    });     
}