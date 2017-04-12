"use strict";

d3.json('/data.json', makeForceGraph); 


function makeForceGraph(error, data) {
    var dataNodes = data.nodes;
    console.log(dataNodes);
    var links = data.paths;
    console.log(links);

    var width = 2000;
    var height = 2000;

    var div = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)

    var force = d3.forceSimulation(d3.values(dataNodes))
        // .force("link", d3.forceLink(links).distance(10).strength(0.25)) //I like the clustering but too close togeter for closely related circles
        .force("link", d3.forceLink(links).distance(45).strength(0.25)) //This gives slightly more breathing room, but some fall off the page
        .force("center", d3.forceCenter(width / 2, height/ 2))
        .force("charge", d3.forceManyBody())
        .on("tick", tick);

    var svg = d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // add the links and the arrows

    var link = svg.selectAll(".link")
        .data(links)
        .enter()
          .append("path")
          .attr("class", "link");

    // define the nodes

    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter()
          .append("g")
          .attr("class", "node")
          .call(d3.drag()
              .on('start', dragstarted)
              .on('drag', dragged)
              .on('end', dragended))
              .on('click', makeSelection)
              .on('mouseover', function(d, i){ 
                    div.transition().style('opacity', 1.0);

                    // Still need to fix style attributes so tooltip shows up 
                    // over d3 viz not above it.
                    div.html("<strong>" + d.title + "</strong>")
                        .style('left', d3.event.pageX + "px")
                        .style('top', d3.event.pageY + "px");
                }) 
              .on('mouseout', function(d, i) {
                  div.transition().style('opacity', 0)
                });


    var color = d3.scaleOrdinal(d3.schemeCategory20b);

    node.append("circle")
        .attr("r", function(d) { return d.num_children})
        .style("fill", function (d) {
          return color(d.title);
        });

    // add the text

    node.append("text")
        .text(function (d) {
            if (d.num_children > 15) { return d.title; }
            })
        .attr('text-anchor', 'middle');

    function tick() {
      link.attr("x1", function (d) {
            return d.source.x;
          })
          .attr("y1", function (d) {
            return d.source.y;
          })
          .attr("x2", function (d) {
            return d.target.x;
          })
          .attr("y2", function (d) {
            return d.target.y;
          });

      node.attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
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
