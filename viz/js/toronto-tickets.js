
var DEFAULT_YEAR = 2011;//start at 2011
var TORONTO_COORDS = [-79.38558, 43.7020];

var WIDTH = document.getElementById('map-container').clientWidth;
var HEIGHT = Math.max(500, window.innerHeight) - 175;
var PREFIX = prefixMatch(['webkit', 'ms', 'Moz', 'O']);

var current_year; // hold tje current year
var fine_amt=0; //hold tje current fine amount filter value
var ticket_freq=0; //hold the current ticket/day filter value

var num_format = d3.format('0,000');

var raw_data; //load parking location data into this variable

var fine_amts; //load json object into this variable for the legend

var infrac_cds;

var filterValues = []; //hold the infraction types user has clicked

//circles sized by total revenue which varies year by year
var rscale; //scale for circle radius to keep max radius constant across each year


var color_scale = d3.scale.category10();

var dateSlider = document.getElementById('date-slider');

var amtSlider = document.getElementById('amt-slider');
var freqSlider = document.getElementById('freq-slider');

function buildSlider() {
  noUiSlider.create(dateSlider, {
  	start: [ DEFAULT_YEAR ],
    connect: 'lower',
    step: 1,
    tooltips: [wNumb({decimals:0})],
  	range: {
  		'min': [  2008 ],
  		'max': [ 2015 ]
  	}
  });

  dateSlider.noUiSlider.on('update', function( values, handle ) {
  	year = parseInt(values[0]);
    update(year);
  });

  noUiSlider.create(amtSlider, {
  	start: 0,
    step: 25,
    connect: 'upper',
  	orientation: 'vertical',
    tooltips: [wNumb({decimal:0, prefix: '$'})],
  	range: {
  		'min': 0,
  		'max': 500
  	}
  });


  noUiSlider.create(freqSlider, {
  	start: 0,
    step: 0.5,
    connect: 'upper',
  	orientation: 'vertical',
    // tooltips: [wNumb({decimal:0, prefix: '#/day > '})],
    tooltips: [wNumb({decimal:1})],
  	range: {
  		'min': 0,
  		'max': 20
  	}
  });


  amtSlider.noUiSlider.on('change', function( values, handle ) {
    // console.log.log('amt slider change')
    fine_amt = parseInt(values[0]);
    data = filterData();
    points();
    add_circles(data);
  });


  freqSlider.noUiSlider.on('change', function( values, handle ) {
    // console.log('freq slider change')
    // console.log(values[0])
    ticket_freq = parseInt(values[0]);
    data = filterData();
    points();
    add_circles(data);
  });
}


// load the fine amounts dictionary dataset
d3.json('/data/fine_amts.json', function(data) {
      // console.log('fine amounts data loaded')
      // console.log(data);
      fine_amts = data;
    });


// load the main dataset
d3.csv('/data/top_spots.csv', function(error, data)
      {
        // console.log('ticket location data loaded')
        // Convert strings to numbers.
        data.forEach(function(d) {
          d.fine_sum = +d.fine_sum;
          d.infraction_code=+d.infraction_code;
          d.count=+d.count;
          d.mean_hour=+d.mean_hour;
          d.freq = Math.round(d.count/365*100)/100
        });
        // console.log(data);
        raw_data = data;
        buildSlider()
        instructions()
      });

var tile = d3.geo.tile()
    .size([WIDTH, HEIGHT]);

var projection = d3.geo.mercator()
    .scale((1 << 20) / 2 / Math.PI)
    .translate([-WIDTH / 2, -HEIGHT / 2]);


//revised: zoom to toronto
var zoom = d3.behavior.zoom()
    .scale(projection.scale() * 2 * Math.PI)
    .scaleExtent([1 << 200, 1 << 25])
    .translate(projection(TORONTO_COORDS).map(function (x) {
        return -x;
    }))
    .on('zoom', zoomed);


var map_container = d3.select('#map-container')
    .style('height', HEIGHT + 'px')
    .call(zoom)
    .on('mousemove', mousemoved); //for coordinates shown on bottom left


var map = map_container.append('g')
    .attr('id', 'map');



var layer = map.append('div')
    .attr('class', 'layer');

var info = map.append('div')
    .attr('class', 'info');

var foreign = d3.select('#legend')
                .append('foreignObject')
                .attr('width', 500)
                .attr('height', HEIGHT - 200)
                .append('xhtml:div')
                .style('max-height', HEIGHT - 200 + 'px')
                .style('max-width', '500px')
                .style('overflow-y', 'scroll')
                .style('overflow-x', 'scroll');


var legend = foreign.append('svg')
                  	.attr('width', 400)
                    // .style('position', 'absolute')
                    // .style('top', 20+'px')
                    // .style('left',10+'px')
                  	.attr('height', 800)
                  	.attr('class','legend');

// define the information displayed in the tooltip
var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return '<span>' + d.street_address + '</span>' + '<br />' + '<span>' +
                        'Total Revenue: $' + num_format(d.fine_sum) + '</span>' + '<br />' + '<span>' +
                        'Tickets/day: ' + d.freq + '</span>' + '<br />' + '<span>' +
                        'Ticket Cost: $' + d.fine_amt +'<br />' + '</span>' +
                        // 'Infraction Type: ' + d.infraction_code + '</span>';
                        d.fine_descrp + '</span>';
              // return '<span style='color:black'>' + d.street_address + '</span>';
            });



// function to remove and re-add points
function points() {
  d3.select('#points').remove();
  var points = map_container.append('svg')
                            .attr('id', 'points');

  // add tips to each point
  points.call(tip);

}


// build a linear radius scale that maps the square root of the value to the radius size
function buildRadius(data) {
  // function modified from:
  // https://bl.ocks.org/guilhermesimoes/e6356aa90a16163a6f917f53600a2b4a
  var maxValue, maxCircleRadius, circleRadiusScale;

  max = d3.max(data, function(d) { return d.fine_sum; });
  min = d3.min(data, function(d) { return d.fine_sum; });
  maxValue = Math.sqrt(max);
  minValue = Math.sqrt(min);

  // maxCircleRadius = d3.min([this.scales.y.bandwidth(), this.scales.x.step()]) / 2;
  circleRadiusScale = d3.scale.linear()
    .domain([minValue, maxValue])
    .range([0.00000075, 0.00001]);

  return function circleRadius (d) {
    return circleRadiusScale(Math.sqrt(d));
  };
}

// function to filter the dataset to the selected year
function update(year) {
  current_year = year;
  data = raw_data.filter(function(d) {
          return d.year == year;});

  //get list of unique infraction_code's for given year
  infrac_cds = d3.map(data, function(d){ return d.infraction_code;}).keys();

  //map the new domain to the color scale
  color_scale = color_scale.domain(infrac_cds)

  //redefine scale based on new data
  rscale = buildRadius(data)

  points();
  add_circles(data);
  build_legend();
}


function add_circles(data) {
  d3.select('#points')
    .selectAll('circle')
    .data(data) //plotted 	locations on map
    .enter()
    .append('circle')
    .attr('class', 'parking_spot')
    .attr('cx', function(d) {return projection([d.lng,d.lat])[0]})
    .attr('cy', function(d) {return projection([d.lng,d.lat])[1]})
    .attr('r',1)
    .style('fill', function(d) {return color_scale(d.infraction_code)})
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide)
    .on('click', streetView);

  // d3.selectAll('circle')
  //     .transition().duration(2000)
  //     .attr('r', function(d) {return rscale(d.fine_sum)*zoom.scale()});

  zoomed();
}


// https://developers.google.com/maps/documentation/javascript/examples/streetview-simple
function streetView(datum) {
  // // console.log(d3.select(this))
  // console.log('loading streetview')
  // console.log(datum)
  $.alert({
    columnClass: 'col-md-8 col-md-offset-2',
    title: datum.street_address, //'Streetview: ' +
    content: '',
    onContentReady: function () {
        var self = this;
        // this.setContent('<div class='col-md-6'><div>id='map' style='height:400px'></div></div>  <div class='col-md-6'><divid='pano' style='height:400px'></div></div>');
        this.setContent('<div id="gmap" style="width:50%; height:400px; float: left;">' +
        '</div> <div id="pano" style="width:50%; height:400px"></div>');
        var location = {lat: parseFloat(datum.lat), lng: parseFloat(datum.lng)};
        console.log(location)

        var map = new google.maps.Map(document.getElementById('gmap'), {
          center: location,
          zoom: 16
        });
        var panorama = new google.maps.StreetViewPanorama(
            document.getElementById('pano'), {
              position: location,
              pov: {
                heading: 0,
                pitch: 0
              }
            });
        map.setStreetView(panorama);


    },
    theme: 'light', // light, supervan, dark
    draggable: true,
    buttons : {close: {text:'Close'}}
  });


}

function filterData() {
  return raw_data.filter(function(d) {
          return filterValues.includes(String(d.infraction_code)) == false
          & d.year==current_year
          & d.fine_amt >= fine_amt
          & d.freq >= ticket_freq
          ;});
}


function deselectAll() {
  filterValues = infrac_cds;
  data = filterData();
  points();
  add_circles(data);
  d3.select('#legend')
    .selectAll('g')
    .style('opacity', 0.2);
}


function selectAll() {
  filterValues = [];
  data = filterData();
  points();
  add_circles(data);
  d3.select('#legend')
    .selectAll('g')
    .style('opacity', 1.0);
}


function legend_filter(e){
  infrac_cd = e;
  if (filterValues.includes(infrac_cd)) {
    d3.select(this).style('opacity', 1.0);
    index = filterValues.indexOf(infrac_cd)
    filterValues.splice(index,1)
    data = raw_data.filter(function(d) {
            return filterValues.includes(String(d.infraction_code)) == false & d.year==current_year;});
    points();
    add_circles(data);
  }
  else {
   d3.select(this).style('opacity', 0.2);
   filterValues.push(infrac_cd)
   data = raw_data.filter(function(d) {
           return filterValues.includes(String(d.infraction_code)) == false & d.year==current_year;;});
   points();
   add_circles(data);
  }
}

//build legend pane
function build_legend(){
  d3.select('#legend').selectAll('g').remove();
  var node_size=15;

  var legend_node = legend.selectAll('.node')
                          .attr('class','node')
                          .data(infrac_cds)
                          .enter().append('g')
                          .attr('transform', function(d, i) {return 'translate(0,' + (i+1) * (node_size*1.5) + ')';})
                          .attr('opacity',1.0)
                          .on('click', legend_filter);

  legend_node.append('rect')
              .attr('class','node')
              .attr('width', node_size)
              .attr('height', node_size)
              .style('fill', function(d) {return color_scale(d);});

  legend_node.append('text')
              .attr('class','node')
              .attr('x', 20)
              .attr('y', node_size/2)
              .attr('dy', '.35em')
              .text(function(d) {
                legend_str=d+': '+fine_amts[d]['fine_descp']+' - $'+fine_amts[d]['fine_amt'];
                return legend_str; });
  }

// this function defines the zoom behaviour of the tiles and cirlces
function zoomed() {

  var tiles = tile
      .scale(zoom.scale())
      .translate(zoom.translate())
      ();

  projection
      .scale(zoom.scale() / 2 / Math.PI)
      .translate(zoom.translate());

  var circles = d3.selectAll('circle')
        .attr('cx', function(d) {return projection([d.lng,d.lat])[0]})
        .attr('cy', function(d) {return projection([d.lng,d.lat])[1]})
        // .transition().duration(2000)
        .attr('r', function(d) {return rscale(d.fine_sum)*zoom.scale()});

  var image = layer
      .style(PREFIX + 'transform', matrix3d(tiles.scale, tiles.translate))
      .selectAll('.tile')
      .data(tiles, function(d) { return d; });

  image.exit()
      .remove();


//https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaWFud2hpdGVzdG9uZSIsImEiOiJjajJqcXY0cGowMDIzMzJueHRkbTdwb3lxIn0.UOywpIDBUqX6my3XaHeKsw'

//play with this to format what OSM gives you...
  image.enter()
      .append('img')
      .attr('class', 'tile')
      .attr('src', function(d) { return 'https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/' + d[2] + '/' + d[0] + '/' + d[1] + '?access_token=pk.eyJ1IjoiaWFud2hpdGVzdG9uZSIsImEiOiJjazlxNmJpM3UwZnE4M2dydHR6bXJiaDcxIn0.xwUBsn91SYMPrNieaXU8Ag'; })
      .style('left', function(d) { return (d[0] << 8) + 'px'; })
      .style('top', function(d) { return (d[1] << 8) + 'px'; });
}

function mousemoved() {
  info.text(projection.invert(d3.mouse(this)));
  info.text(formatLocation(projection.invert(d3.mouse(this)), zoom.scale()));
}

function matrix3d(scale, translate) {
  var k = scale / 256, r = scale % 1 ? Number : Math.round;
  return 'matrix3d(' + [k, 0, 0, 0, 0, k, 0, 0, 0, 0, k, 0, r(translate[0] * scale), r(translate[1] * scale), 0, 1 ] + ')';
}

function prefixMatch(p) {
  var i = -1, n = p.length, s = document.body.style;
  while (++i < n) if (p[i] + 'Transform' in s) return '-' + p[i].toLowerCase() + '-';
  return '';
}

function formatLocation(p, k) {
  var format = d3.format('.' + Math.floor(Math.log(k) / 2 - 2) + 'f');
  return (p[1] < 0 ? format(-p[1]) + '°S' : format(p[1]) + '°N') + ' '
       + (p[0] < 0 ? format(-p[0]) + '°W' : format(p[0]) + '°E');
}

// function to display a pop up box with instructions
function instructions() {
  $.alert({
    title: 'Instructions',
    content: '<li>Hover over any of the circles for a summary of that location</li>' +
    '<li>Each circle is sized according to the revenue of that location. Larger circles represent spots that accumulated more revenue</li>'+
    '<li>Click on a circle to see the Google Maps Streetview (location is not always correct, use the slider to adjust the streetview positioning)</li>'+
    '<li>Use the horizontal slider at the top of the page to change the year</li>'+
    '<li>Use the vertical sliders to filter by ticket amount, or number of tickets per day</li>'+
    '<li>Click on parking ticket types in the legend to toggle their inclusion on the map</li>',
  });
}
