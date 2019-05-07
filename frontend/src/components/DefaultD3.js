import React, { Component } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';

class DetaultD3 extends Component {

  constructor(props) {
    console.log("constructor()")
    super(props)
    this.state = {
      topologyData: null,
      unemploymentData: null
    }
  }

  componentWillMount() {
    console.log("componentWillMount()")

    Promise.all(
      [d3.json("https://d3js.org/us-10m.v1.json"),
      d3.tsv("../static/unemployment.tsv")]
    ).then( ([topologyData, unemploymentData]) => {
          this.setState({
            topologyData,
            unemploymentData
          })
    }).catch(err => console.log('Error loading or parsing data.'))

  }

  componentDidUpdate() {
    console.log("componentDidUpdate()")

    const svg = d3.select(this.refs.anchor),
      { width, height } = this.props;

    const path = d3.geoPath();
    const unemployment = d3.map();

    unemployment.set(this.state.unemploymentData.id, +this.state.unemploymentData.rate);

    const x = d3.scaleLinear()
        .domain([1, 10])
        .rangeRound([400, 860]);

    const color = d3.scaleThreshold()
        .domain(d3.range(2, 10))
        .range(d3.schemeBlues[9]);

    const g = svg.append("g")
        .attr("class", "key")
        .attr("transform", "translate(0,40)");

    g.selectAll("rect")
      .data(color.range().map(function(d) {
          d = color.invertExtent(d);
          if (d[0] == null) d[0] = x.domain()[0];
          if (d[1] == null) d[1] = x.domain()[1];
          return d;
        }))

    const usStates = topojson.feature(this.state.topologyData, this.state.topologyData.objects.states).features
    const usStatePaths = topojson.mesh(this.state.topologyData, this.state.topologyData.objects.states, function(a, b) { return a !== b; });

    svg.append("g")
      .attr("class", "states")
      .selectAll("path")
      .data(usStates)
      .enter().append("path")
        .attr("fill", function(d) { return color(d.rate = unemployment.get(d.id)); })
        .attr("d", path)
      .append("title")
        .text(function(d) { return d.rate + "%"; })
      .attr("d", path);


    svg.append("path")
      .attr("class", "state-borders")
      .attr("d", path(usStatePaths));

  }

  render () {
    console.log("render()")
    const { topologyData, unemploymentData } = this.state;

    if(!topologyData || !unemploymentData) {
       return null;
    }

    return <g ref="anchor" />;
  }
}

export default DetaultD3;
