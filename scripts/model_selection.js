
var form=document.getElementById("form1");
    form.onsubmit = function (e) {
        e.preventDefault();
        
    update1();

    }

var ht_data=[];    
var server = "http://35.227.40.171:8080"
var def_url1= "/cf_eval/preprocessing=Numeric&model=SVD_explicit&dim=40&top_k=10"
var get_data1 = function(pvals, mvals, ldvals, mt, callback) {
    $('#loader2').show();
    if($.isEmptyObject(ht_data)){

    $.getJSON(server+def_url1).then(function (data) {
                ht_data = JSON.parse(JSON.stringify(data));
                console.log("Precomputed data loaded.");
                callback(ht_data);
            });
    }
    else {
//        var fdata=ht_data.filter(function(i){
//                return ($.inArray(i.Model, mvals) != -1 && $.inArray(String(i.Preprocessing), pvals) != -1);
//            });
//        var dlds = [];
//            fdata.map(function(d) {
//                    dlds.push(String(d.LatentDimensions));
//                });
//        let a = new Set(ldvals);
//        let b = new Set(dlds);
//        var difference = Array.from(
//            [...a].filter(x => !b.has(x)));
//        console.log(difference);
//        
//        if($.isEmptyObject(difference)){
            callback(ht_data);  
//        }
//        else {
//            console.log("This is going to take time.");
//            
//            for(var ld=0; ld<difference.length;ld++){
//                for(var m=0; m<mvals.length;m++){
//                    for(var p=0; p<pvals.length;p++){
//                       var url= '/cf_eval/preprocessing='+pvals[p]+'&model='+mvals[m]+'&dim='+difference[ld]+'&top_k=10'
//                       console.log(url);
//                        
//                         $.getJSON(server+url).then(function (data) {
//                            var ld_data = JSON.parse(JSON.stringify(data));
//                              console.log(ld_data.length);
//                            ld_data = ld_data[ld_data.length-1]; 
//                              console.log(ld_data);
//                              console.log(ht_data.length);
//                            ht_data.push(ld_data);  
//                              console.log(ht_data.length);
//                            callback(ht_data); 
//                       });   
//                        
//                    }
//                }
//            }
//        }
    }
    
    }

var update1 = function() {

    var pvals = $('#preprocessing').val();
//    console.log(pvals);
    var mvals = $('#model').val();
//    console.log(mvals);
    var ldvals = $('#ld').val();
    console.log("ldvals: ", ldvals);
    var mt = $('#metric').val();
//    console.log(mt);
    
    get_data1(pvals, mvals, ldvals, mt, function(ht_data){
    
  
    var data=ht_data.filter(function(i){
                        return ($.inArray(i.Model, mvals) != -1 && $.inArray(String(i.Preprocessing), pvals) != -1 && $.inArray(String(i.LatentDimensions), ldvals) != -1 );
                    });

    var ht_layout = {
          grid: {
            rows: 1,
            columns: mvals.length,
            subplots:[]
          },
        annotations:[{
            xref: 'paper',
            yref: 'paper',
            x: 0,
            xanchor: 'right',
            y: 1,
            yanchor: 'bottom',
            text: mt[0],
            showarrow: false
          }, {
            xref: 'paper',
            yref: 'paper',
            x: 1,
            xanchor: 'left',
            y: 0,
            yanchor: 'top',
            text: 'Latent Dimensions',
            showarrow: false
          }],
        margin: {l: 100,r: 140,b: 40,t: 40,pad: 0}
        };
    var ms_layout = {
        margin: {l: 100,r: 140,b: 40,t: 40,pad: 0},
        annotations:[{
            xref: 'paper',
            yref: 'paper',
            x: 0,
            xanchor: 'right',
            y: 1,
            yanchor: 'bottom',
            text: mt[0],
            showarrow: false
          }, {
            xref: 'paper',
            yref: 'paper',
            x: 1,
            xanchor: 'left',
            y: 0,
            yanchor: 'top',
            text: 'Models',
            showarrow: false
          }]
        };

    var ht_traces = [];
    var ms_traces = [];
    var colors = ["#1f77b4", "#2ca02c"]
    var bool = [true, false]
    for(var m=0; m<mvals.length;m++){
        for(var p=0; p<pvals.length;p++){

        var mdata=data.filter(function(i){
                        return i.Model==mvals[m] && i.Preprocessing==pvals[p];         
                    });

        var mtvals = [];
        mdata.map(function(d) {
                mtvals.push(d[mt[0]]);
            });

        var ht_trace = {
          x: ldvals,
          y: mtvals,
          xaxis: 'x'+String(m+1),
          yaxis: 'y',
          name: pvals[p],
          type: 'scatter',
          marker: {
                color: colors[p]
              },
              line: {
                color: colors[p]
              },
         legendgroup: 'group'+String(p),
         showlegend: bool[m]

        };
        ht_traces.push(ht_trace);


        var ms_trace = { 
          x: mvals[m],  
          y: mtvals,
          name: mvals[m],
          type: 'violin',
          marker: {
                color: colors[p]
              },
          legendgroup: 'group'+String(p),
          showlegend: bool[1]
        };
        ms_traces.push(ms_trace); 
        }

    ht_layout["xaxis"+String(m+1)] = {title: mvals[m]};
    ht_layout["grid"]["subplots"].push = "x"+m+"y";
    }

    $('#loader2').hide();
    Plotly.newPlot('htchart', ht_traces, ht_layout);
    Plotly.newPlot('mschart', ms_traces, ms_layout);


    var best = data.sort((a, b) => parseFloat(b[mt[0]]) - parseFloat(a[mt[0]]))[0];

    $("#bpreprocessing").text(String(best.Preprocessing));
    $("#bmodel").text(String(best.Model));
    $("#bld").text(String(best.LatentDimensions));

 
    });
          
        
}