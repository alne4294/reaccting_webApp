

// custom javascript
$(function() {
  console.log('jquery is working!');
  findOne();
  createFindGraph();
});

//=======================================================
function findOne(){

	d3.json("/api/1.0/mongoWebApp/findOne", function(docs) {
	  
		data = jQuery.parseJSON(docs.data);

		var temp = data.temperature;
		var light = data.light;
		var isoDate = data.iso_dt;
		var iso_date = new Date(isoDate.$date);
		var humidity = data.humidity;
		var device = data.device;
		var dt = data.dt;
	  
	  	console.log("findOne() Results: ---------------");
		console.log(temp);
		console.log(light);
		console.log(iso_date);
		console.log(humidity);
		console.log(device);
		console.log(dt);
	});

}


//=======================================================
function createFindGraph() {

	var dataset = [];
	var numDataPoints = 0;	

	d3.json("/api/1.0/mongoWebApp/find", function(docs) {
	  
		dataArray = docs.data;
		numDataPoints = dataArray.length;

		for (var i = 0; i < numDataPoints; i++){
			doc = jQuery.parseJSON(dataArray[i]);
			// console.log(doc)

			var isoDate = doc.iso_dt;
			// console.log(isoDate.$date);
			var iso_date = new Date(isoDate.$date);
			// console.log("Date object: " );
			// console.log(iso_date);

			var temp = doc.temperature;
			
			var newNumber1 = iso_date;
			var newNumber2 = temp;
			
			dataset.push([newNumber1, newNumber2]);

		}

		//Call here (within callback function) because 
		//it's dependent on the asynchronous call
		graphResults(dataset, numDataPoints);
	  
	});
}

//=======================================================
function graphResults(dataset, numDataPoints){

	// console.log("NUM DATA POINTS")
	// console.log(numDataPoints)

	//Width and height
	var w = 600;
	var h = 400;
	var padding = 30;
	
	//Create scale functions
	lowerX = d3.min(dataset, function(d) { return d[0]; })
	// console.log(lowerX);
	upperX = d3.max(dataset, function(d) { return d[0]; })
	// console.log(upperX);
	var xScale = d3.scale.linear()
						 .domain([lowerX, upperX])
						 .range([padding, w - padding * 2]);
	lowerY = d3.min(dataset, function(d) { return d[1]; })
	console.log(lowerY);
	upperY = d3.max(dataset, function(d) { return d[1]; })
	console.log(upperY);
	var yScale = d3.scale.linear()
						 .domain([lowerY, upperY])
						 .range([h - padding, padding]);
	//Define X axis
	var xAxis = d3.svg.axis()
					  .scale(xScale)
					  .orient("bottom")
					  .ticks(5);
	//Define Y axis
	var yAxis = d3.svg.axis()
					  .scale(yScale)
					  .orient("left")
					  .ticks(5);
	//Create SVG element
	var svg = d3.select("body")
				.append("svg")
				.attr("width", w)
				.attr("height", h);
	//Create circles
	svg.selectAll("circle")
	   .data(dataset)
	   .enter()
	   .append("circle")
	   .attr("cx", function(d) {
	   		return xScale(d[0]);
	   })
	   .attr("cy", function(d) {
	   		return yScale(d[1]);
	   })
	   .attr("r", 2);
	
	//Create X axis
	svg.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + (h - padding) + ")")
		.call(xAxis);
	
	//Create Y axis
	svg.append("g")
		.attr("class", "y axis")
		.attr("transform", "translate(" + padding + ",0)")
		.call(yAxis);

	//On click, update with new data			
	d3.select(".find")
		.on("click", function() {
			
			//Update scale domains
			xScale.domain([d3.min(dataset, function(d) { return d[0]; }), d3.max(dataset, function(d) { return d[0]; })]);
			yScale.domain([0, d3.max(dataset, function(d) { return d[1]; })]);
			//Update all circles
			svg.selectAll("circle")
			   .data(dataset)
			   .transition()
			   .duration(1000)		
			   .attr("cx", function(d) {
			   		return xScale(d[0]);
			   })
			   .attr("cy", function(d) {
			   		return yScale(d[1]);
			   });
			//Update X axis
			svg.select(".x.axis")
		    	.transition()
		    	.duration(1000)
				.call(xAxis);
			
			//Update Y axis
			svg.select(".y.axis")
		    	.transition()
		    	.duration(1000)
				.call(yAxis);
		});

	// var width = 960; // chart width
	// var height = 700; // chart height
	// var format = d3.format(",d");  // convert value to integer
	// var color = d3.scale.category20();  // create ordinal scale with 20 colors
	// var sizeOfRadius = d3.scale.pow().domain([-100,100]).range([-50,50]);  // https://github.com/mbostock/d3/wiki/Quantitative-Scales#pow

	// var bubble = d3.layout.pack()
	//   .sort(null)  // disable sorting, use DOM tree traversal
	//   .size([width, height])  // chart layout size
	//   .padding(1)  // padding between circles
	//   .radius(function(d) { return 20 + (sizeOfRadius(d) * 30); });  // radius for each circle

	  
	// var svg = d3.select("#chart").append("svg")
	//   .attr("width", width)
	//   .attr("height", height)
	//   .attr("class", "bubble");

	// //REQUEST THE DATA
	// d3.json("/api/1.0/mongoWebApp/findOne", function(docs) {
	//   console.log(docs)
	//   if (docs.error) return console.warn(error);
	//   var node = svg.selectAll('.node')
	//     .data(bubble.nodes(docs)
	//     .filter(function(d) { return !d.children; }))
	//     .enter().append('g')
	//     .attr('class', 'node')
	//     .attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'});

	//     node.append('circle')
	//       .attr('r', function(d) { return d.r; })
	//       .style('fill', function(d) { return color(d.symbol); });

	//     node.append('text')
	//       .attr("dy", ".3em")
	//       .style('text-anchor', 'middle')
	//       .text(function(d) { return d.symbol; });
	// });

	// // tooltip config
	// var tooltip = d3.select("body")
	//   .append("div")
	//   .style("position", "absolute")
	//   .style("z-index", "10")
	//   .style("visibility", "hidden")
	//   .style("color", "white")
	//   .style("padding", "8px")
	//   .style("background-color", "rgba(0, 0, 0, 0.75)")
	//   .style("border-radius", "6px")
	//   .style("font", "12px sans-serif")
	//   .text("tooltip");


	// node.append("circle")
	//   .attr("r", function(d) { return d.r; })
	//   .style('fill', function(d) { return color(d.symbol); })

	//   .on("mouseover", function(d) {
	//     tooltip.text(d.name + ": $" + d.price);
	//     tooltip.style("visibility", "visible");
	//   })
	//   .on("mousemove", function() {
	//     return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
	//   })
	//   .on("mouseout", function(){return tooltip.style("visibility", "hidden");});
}