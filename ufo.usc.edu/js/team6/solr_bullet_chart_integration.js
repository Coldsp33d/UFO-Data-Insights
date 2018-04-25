var SOLR_BASE_URL = "http://localhost:8983/solr/ufo/select";

var SOLR_GROUP_BY_STATES_QUERY_PARAM = {
	fl:'state',
	'group.field':'state',
	group:true,
	q:'state:*',
	rows:100,
	wt:'json'
}

var SOLR_FACET_START_RANGE = "2000-01-01T00:00:00.00Z"
var SOLR_FACET_END_RANGE = "2010-01-01T00:00:00.00Z"
var SOLR_FACET_COLUMN = "sighted_at"
var SOLR_RANGE_DURATION = "+5YEAR"

var SOLR_FACET_DATA_QUERY_PARAM = {
	"facet.range.gap":SOLR_RANGE_DURATION,
	"rows":"0",
	"facet":"true",
	"facet.range.start": SOLR_FACET_START_RANGE,
	rows: 0,
	"facet.range.end": SOLR_FACET_END_RANGE,
	"facet.range": SOLR_FACET_COLUMN
}

populate_state_dropdown = function(data) {
	var states = data.grouped.state.groups;
	var states_arr = [];
	for (var i = 0; i < states.length; i++) {
		states_arr.push(states[i].groupValue);
		$("#sel1").append('<option>' + states[i].groupValue +'</option>');
	}
	reload_bullet(true);
}

jQuery.ajax({
  url: SOLR_BASE_URL,
  data: SOLR_GROUP_BY_STATES_QUERY_PARAM,
  success: populate_state_dropdown,
  dataType: 'jsonp',
  jsonp: 'json.wrf'
});

var margin = {top: 5, right: 40, bottom: 20, left: 120},
    width = 960 - margin.left - margin.right,
    height = 50 - margin.top - margin.bottom;

var chart = d3.bullet()
    .width(width)
    .height(height);


var fetched_all_data = function(shouldInitialize) {
	
	if(shouldInitialize) {
		var svg_d = [];
		for(shape in shapes) {
			svg_d.push(shapes[shape]);
		}
		initialize(svg_d);
	}
	else {
		var svg_d = svg.data();
		for(var i = 0; i < svg_d.length; i++) {
			svg_d[i] = shapes[svg_d[i].title.toLowerCase()];
		}
		svg.data(svg_d).call(chart.duration(1000));
	}
}

var shapes = {'light':{}, 'triangle':{}, 'fireball':{}, 'sphere':{}, 'disk':{}};
var len_shapes = 5;



$( "#sel1" ).change(function() {
	reload_bullet(false);
});

var reload_bullet = function (initialize) {
	var state = $("#sel1").val();
	var svg_d_ct = 0;
	for (shape in shapes) {
		SOLR_FACET_DATA_QUERY_PARAM.q = "shape:" + shape;
		SOLR_FACET_DATA_QUERY_PARAM.fq = "state:"+state;
		jQuery.ajax({
			url: SOLR_BASE_URL,
			data: SOLR_FACET_DATA_QUERY_PARAM,
			success: function(response_data) {
				var title = response_data.responseHeader.params.q.split(":")[1];
				var count_1 = response_data.facet_counts.facet_ranges.sighted_at.counts[1]
				var count_2 = response_data.facet_counts.facet_ranges.sighted_at.counts[3];
				var total = count_1 + count_2
				var d = {
							"title":title,
							"subtitle":"",
							"ranges":[count_1,total],
							"measures":[count_2],
							"markers":[0]
						}
				svg_d_ct += 1
				shapes[title] = d;
				if(svg_d_ct == len_shapes) {
					fetched_all_data(initialize);
				}
			},
			dataType: 'jsonp',
			jsonp: 'json.wrf'
		});
	}
}

function initialize(data) {
	svg = d3.select("#bullet-chart").selectAll("svg")
      .data(data)
    .enter().append("svg")
      .attr("class", "bullet")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(chart);

  var title = svg.append("g")
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + height / 2 + ")");

  title.append("text")
      .attr("class", "title")
      .text(function(d) { return d.title.charAt(0).toUpperCase() + d.title.slice(1); });
}