"use strict";

var color = d3.scaleOrdinal(d3.schemeCategory20b);
var svg = d3.select('svg');    

var width = 2000;
var height = 2000;

var simulation = d3.forceSimulation()
    // .force("link", d3.forceLink(links).distance(10).strength(0.25)) //I like the clustering but too close togeter for closely related circles
    .force("link", d3.forceLink().distance(20).strength(0.2)) //This gives slightly more breathing room, but some fall off the page
    .force("center", d3.forceCenter(width / 2, height/ 2))
    .force("charge", d3.forceManyBody());


var div = d3.select('body').append('div')
    .attr('class', 'tooltip tooltip-text')
    .style('opacity', 0)


d3.json('/data.json', makeForceGraph); 


function makeForceGraph(error, data) {

    console.log('ORIGINAL DATA', data);
    var  nodes = data.nodes;
    var  nodeById = d3.map(nodes, function(d) { return d.slug; });
    var  links = data.paths;
    var  bilinks = [];
    console.log('ORIGINAL NODES": ', nodes);
    console.log('original links:', links);

    links.forEach( function(link) {
      var s = link.source = nodeById.get(link.source);
      var t = link.target = nodeById.get(link.target);
      var i = {};
      nodes.push(i);
      links.push({source: s, target: i}, {source: i, target: t});
      bilinks.push([s, i, t]);
    });
 
    console.log('NEW NODES:', nodes);
    console.log('NEW LINKS:', links);
    console.log('BILINKS:', bilinks);

    var link = svg.selectAll(".link")
        .data(bilinks)
        .enter()
          .append("path")
          .attr("class", "link")
          .attr('stroke', 'gray')
          .attr('stroke-width', '0.5px');

    var node = svg.selectAll(".node")
        .data(nodes.filter(function(d) { return d.slug; }))
        .enter()
          .append("g")
          .attr("class", "node")
          .call(d3.drag()
              .on('start', dragstarted)
              .on('drag', dragged)
              .on('end', dragended))
              .on('click', makeSelection)
              .on('mouseover', function(d, i){ 
                    if (d.num_children <= 15) {
                      div.transition().style('opacity', 1.0);

                      // Still need to fix style attributes so tooltip shows up 
                      // over d3 viz not above it.
                      div.html("<strong>" + d.title + "</strong>")
                          .style('left', (d.x - d.num_children) + "px")
                          .style('top', (d.y - d.num_children) + "px");
                    }
                }) 
              .on('mouseout', function(d, i) {
                  div.transition().style('opacity', 0)
                });

    node.append("circle")
        .attr("r", function(d) { return d.num_children})
          .on('mouseover', function(d, i) {
            d3.select(this).transition().attr('r', function(d) { return d.num_children * 1.5})
          })
          .on('mouseout', function(d, i) {
            d3.select(this).transition().attr('r', function(d) { return d.num_children })
          })
        .style("fill", function (d) {
          return color(d.title);
        });

    // add the permanent text
    node.append("text")
        .text(function (d) {
            if (d.num_children > 15) { return d.title; }
            })
        .attr('text-anchor', 'middle')
        .attr('class', 'tooltip-text')
        .attr('class', 'show');

    simulation
      .nodes(nodes)
      .on('tick', ticked);

    simulation.force('link')
      .links(links);

    function ticked() {
      link.attr("d", positionLink);
      node.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
    }
    
    function positionLink(d) {
      return "M" + d[0].x + "," + d[0].y
           + "S" + d[1].x + "," + d[1].y
           + " " + d[2].x + "," + d[2].y;
    }

    function dragstarted(d) {
      if (!d3.event.active) {
        force.alphaTarget(0.3).restart();
      }
    }
        
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }
        
    function dragended(d) {
      if (!d3.event.active) {
        force.alphaTarget(0);
      }
      d.fx = null;
      d.fy = null;
    }

    function makeSelection(d) {
        var time_preference = $(':checked').val();
        console.log(time_preference);
        $.get('/find_video', {'slug': d.slug, 'time': time_preference }, function(response) {
            console.log(response);
            $('#videoName').text(response['title']);
            $('#videoDuration').text(response['duration']);
            $('#videoDesc').text(response['description']);  
            $('#videoThumbnail').attr('src', response['image_url']);
            $('.videoLink').attr('href', response['ka_url']);
            $('#videoModal').modal('toggle');
        });
    }
}