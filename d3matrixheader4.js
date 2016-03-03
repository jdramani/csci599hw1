
window.onload = function () {

   
        d3.csv('data.csv', function (data) {
           
            var label_col_full = Object.keys(data[0]);
            var label_row = [];
            var rows = [];
            var row = [];
            for (var i = 0; i < data.length-1; i++) {
                label_row.push(data[i][label_col_full[0]]);
                row = [];
                for (var j = 1; j < label_col_full.length; j++) {
                    row.push(parseFloat(data[i][label_col_full[j]]));
                }
                rows.push(row);
            }
            
            
            main(rows, label_col_full.slice(1), label_row);
            
        });
    };

var mapsize = 1000;
var pixelsize = 2;



d3.select('.tooltip').style('padding',' 10px')
.style('background',' white')
.style('border-radius',' 10px')
.style('box-shadow',' 4px 4px 10px rgba(0, 0, 0, 0.4)');

var main = function (corr, label_col, label_row) {

    var transition_time = 1500;
    var body = d3.select('body');
	body.select('g.legend').style('position','absolute')
	.style('height','25px')
	.style('width','400px').style('margin','auto').style('margin-left','100px')        
	.style('background','linear-gradient(to right,red,white,green)');
    var tooltip = body.select('div.tooltip');
    var svg = body.select('#chart').append('svg')
        .attr('width', mapsize)
        .attr('height', mapsize).style('margin','auto').style('margin-top','-50px').style('margin-left','-50px');;;

  
    var row = corr;
    var col = d3.transpose(corr);


    var indexify = function (mat) {
        var res = [];
        for (var i = 0; i < mat.length; i++) {
            for (var j = 0; j < mat[0].length; j++) {
                res.push({
                    i: i,
                    j: j,
                    val: mat[i][j]
			
                });
		
            }
	
        }
        return res;
    };

    var corr_data = indexify(corr);
    var order_col = d3.range(label_col.length + 1);
    var order_row = d3.range(label_row.length + 1);

    var color = d3.scale.linear()
        .domain([-1, 0, 1])
        .range(['red', 'white', 'green']);

    var scale = d3.scale.linear()
        .domain([0, d3.min([50, d3.max([label_col.length, label_row.length, 4])])])
        .range([0, parseFloat(1) * 250]);

   

    var label_space = 50;

    var matrix = svg.append('g')
        .attr('class', 'matrix')
	.attr('height',mapsize)
	.attr('width',mapsize)
        .attr('transform', 'translate(' + (label_space + 10) + ',' + (label_space + 10) + ')')
	.selectAll('rect.pixel').data(corr_data)
	.enter().append('rect')
        .attr('class', 'pixel')
        .attr('width', pixelsize)
        .attr('height', pixelsize)
	.attr('position','absolute')
	.attr('y',function(d){return d.i*pixelsize+ label_space})
	.attr('x',function(d){return d.j*pixelsize + label_space})
        .style('fill', function (d) {
            return color(d.val);
        })
        .on('mouseover', function (d) {
	     if(d.i > d.j){
             tooltip.style("opacity", 0.8)
	    .style('position', 'absolute')
            .style("left", (d3.event.pageX + 35) + 'px')
            .style("top", (d3.event.pageY + 30) + 'px')
            .html('i:'+ d.i +"," + "j:" +d.j + "," + "Avg_Byte_Freq_Diff:" + d.val.toFixed(3));
		}
             else if(d.i < d.j){
             tooltip.style("opacity", 0.8)
	    .style('position', 'absolute')
            .style("left", (d3.event.pageX + 35) + 'px')
            .style("top", (d3.event.pageY + 30) + 'px')
            .html('i:'+ d.i +"," + "j:" +d.j + "," + "Correlation_Strength:" + d.val.toFixed(3));

	    }
           else
		{
                 
		}
		

		d3.select(this).style("opacity", 0.5);
        })
        .on('mouseout', function (d) {
            tooltip.style("opacity", 1e-6);
	    d3.select(this).style("opacity", 1);
        });
   

rowLabel = []
colLabel = []

for(var m=0; m<256;m++)
{

colLabel.push('b'+m);
}

rowLabel = ['p0','p1','p1','p3']
var rowLabels = svg.append("g")
      .selectAll(".rowLabelg")
      .data(rowLabel)
      .enter()
      .append("text")
      .attr("class","rowLabelg")
      .text(function (d) { return d; })
      .style('font-size','1px')
      .attr("x", 0)
      .attr("y", function (d, i) { return i * pixelsize; })
      .style("text-anchor", "end")
      .attr("transform", "translate(110,111)");
     

  var colLabels = svg.append("g")
      .selectAll(".colLabelg")
      .data(colLabel)
      .enter()
      .append("text")
      .attr("class","colLabelg")
      .text(function (d) { return d; })
      .style('font-size','1px')
      .attr("x", 0)
      .attr("y", function (d, i) { return i * pixelsize; })
      .style("text-anchor", "left")
      .attr("transform", "translate(111,110) rotate (-90)");



}
      
      
