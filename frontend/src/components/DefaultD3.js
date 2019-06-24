import React, { Component } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';

import * as unemploymentTsv from './tempData/unemployment.tsv'

class DetaultD3 extends Component {

  constructor(props) {
    console.log("constructor()")
    super(props)
    this.state = {
      topologyData: null,
      unemploymentData: null
    }
  }

  async componentWillMount() {
    console.log("componentWillMount()");

    try {
      const topoLocation = "https://d3js.org/us-10m.v1.json";
      const topologyData = await d3.json(topoLocation);
  
      const unemploymentData = await d3.tsv(unemploymentTsv);
      console.log(unemploymentData)
  
      this.setState({
        topologyData,
        unemploymentData
      })
    } catch (error) {
      console.log('Error loading or parsing data.')
    }
  }

  componentDidUpdate() {
    console.log("componentDidUpdate()")

    const svg = d3.select(this.refs.anchor),
      { width, height } = this.props;

    const path = d3.geoPath();
    const unemployment = d3.map();
    
    //go through each county in the unemployment data and set the map
    this.state.unemploymentData.forEach((countyData)=>{
      unemployment.set(countyData.id, +countyData.rate);
    })

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

    const usCounties = topojson.feature(this.state.topologyData, this.state.topologyData.objects.counties).features
    const usStatePaths = topojson.mesh(this.state.topologyData, this.state.topologyData.objects.states, function(a, b) { return a !== b; });

    svg.append("g")
      .attr("class", "states")
      .selectAll("path")
      .data(usCounties)
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
