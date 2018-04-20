(function(){
	var width = window.innerWidth,
	height = window.innerHeight;
	var tooltip = d3.select("body")
 	 .append("div")
  	.attr('class', 'tooltip');

	var svg = d3.select("body")
  	.append("svg")
  	.attr("width", width)
  	.attr("height", height);

	


	var radiusScale = d3.scaleSqrt().domain([2,7562]).range([15,85])
	var color = d3.scaleOrdinal(d3.schemeCategory20);
	//the simulation is a collection of forces 
	//about where we want our circles to go
	//and how we want our circle to interact
	//STEP ONE: get them to the middle
	//STEP TWO: dont't have them to collide
	var simulation = d3.forceSimulation()
	.force("x",d3.forceX(width/2).strength(0.05))
	.force("y",d3.forceY(height/2).strength(0.05))
	.force("collide",d3.forceCollide(function(d){
		return radiusScale(d.count) + 1;
	}))
	data  =d3.queue()
	.defer(d3.csv,"../Data/bubble_chart_sightings.csv")
	.await(ready)

	function ready(error,datapoints){

		var circles = svg.selectAll("circle")
		.data(datapoints)
		.enter().append("circle")
		.attr("class","artist")
		.attr("r",function(d){
			return radiusScale(d.count)
		})
		.attr("fill",function(d,i){return color(i);})
		.on('click',function(d){
			console.log(d)
		})
		.on("mouseover", function(d) {
   		 return tooltip.style("visibility", "visible").text('sighted at = ' + d.state);
  		})
  		 .on("mousemove", function() {
    	return tooltip.style("top", (event.pageY - 30) + "px")
      	.style("left", event.pageX + "px");
  		})
  
  		// we hide our tooltip on "mouseout"
  
  		.on("mouseout", function() {
    		return tooltip.style("visibility", "hidden");
  		});

  		var texts= svg.selectAll("text").data(datapoints).enter().append("text");

		simulation.nodes(datapoints)
		.on('tick',ticked)

		function ticked(){
			circles
			.attr("cx", function(d){
				return d.x
			})
			.attr("cy",function(d){
				return d.y
			})
			texts.attr('dy',function(d){
				return d.y
			})
			texts.text(function(d){
				return d.abbr
			})
			texts.attr('dx',function(d){
				return d.x
			})
			texts.attr('font-family','Arial')
		}

	}
})();