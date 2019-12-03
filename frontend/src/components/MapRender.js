import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import { countyList } from './utils/counties';
import { width, height, path, initSW, } from './DefaultD3';

// todo: change color scale from blue
const colorScale = (maxScore) => {
  const iteration = 10;
  const csStart = '#FFFFFF';
  const csEnd = '#2O4177';
  const colorScale = d3.quantize(d3.interpolateHcl(csStart,csEnd), iteration);
  return d3.scaleThreshold().domain(d3.range(0,maxScore, maxScore/(iteration+1)))
    .range(colorScale);
};

const handleHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", 4 * initSW + "px");
};

const removeHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", initSW + "px");
};

export const MapRender = (props) => {
  const anchor = useRef('map-container');
  const { 
    topologyData,
    waterScoreData,
    stateWaterQualData,
    addCounty,
    maxScore,
    centerState,
    usStates,
    areaInViewPort,
  } = props;
  const svg = useRef(null);
  const usCounties = useRef(null);
  const stateFacilityObj = useRef({});
  //refs, we don't want a rerender when these change!
  const g = useRef(null);

  useEffect(() => {
    const translateData = () => {
      // todo: make map render (12/2)
      //set the svg to the anchor element
      svg.current = d3.select(anchor.current).append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`);
      //create an element d3 map
      const waterScore = d3.map();
      //go through each state in the unemploymentByState data and set the map
      for (let i = 0; i < waterScoreData.length; i += 1) {
        const countyWaterScore = waterScoreData[i];
        waterScore.set(countyWaterScore.fips_county_id, +parseFloat(countyWaterScore.score).toFixed(2) * 100);
        const stateId = countyWaterScore.fips_state_id;
        const { facilities } = countyWaterScore;
        if (!stateFacilityObj.current[stateId]) {
          stateFacilityObj.current[stateId] = { facArr: [] };
        }
        if (!facilities)
          continue;
        const { facArr } = stateFacilityObj.current[stateId];
        facArr.push(...facilities);
        stateFacilityObj.current[stateId].facArr = facArr;
      };
      //this is the color scheme and scale
      const noColor = 'rgb(248,249,250)';
      const color = colorScale(maxScore);
      //this creates the data for the map
      usCounties.current = topojson.feature(topologyData, topologyData.objects.counties);
      g.current = svg.current.append("g");
      //we append a new "g" element that will have all the county information
      g.current.append("g")
        //we set the class as "counties" for this element
        .attr("id", "counties")
        // with no path elements, the .data call will create them
        .selectAll("path")
        .data(usCounties.current.features)
        // enter goes into the recently selected elemnt
        .enter().append("path")
        .attr("d", path)
        .attr("id", d => `county-${d.id}`)
        .attr("fill", d => waterScore.get(d.id) ? color(d.score = waterScore.get(d.id)) : noColor)
        .attr("class", "county-boundary")
        .style("stroke", "grey")
        // add county to list
        .on("click", addCounty)
        //the following two lines darken the county that is hovered on
        .on("mouseover", d => handleHover(`county-${d.id}`))
        .on("mouseout", d => removeHover(`county-${d.id}`))
        // this is the hover overlay
        .append("title").text(d => (countyList[d.id] ? countyList[d.id].Name : "Unknown") + ": " + (d.score ? d.score : 0) + "%");
      //can't use "mesh" because we want to create a zoom on state boundary function
      usStates.current = topojson.feature(topologyData, topologyData.objects.states);
      //todo: add dots for facility locations
      //todo: highlight major cities (save for later)
      //todo: move state selector to above the county table
      //todo: add timeline to where state selector is currently
      //we append a new "g" element for the state boundaries
      g.current.append("g")
        //set the class
        .attr("id", "states")
        //select the "path" elements
        .selectAll("path")
        //give our new element the "data"
        .data(usStates.current.features)
        .enter().append("path")
        //create each state's individual path
        .attr("d", path)
        //give each path a boundary for easy coloring
        .attr("class", "state-boundary")
        //add a fully opaque fill, allows the state to handle click
        .attr("fill", "rgba(0,0,0,0)")
        .attr("id", d => `state-${d.id}`)
        .style("stroke", "black")
        .style("stroke-width", ".5px")
        //give a click listener for each state-boundary
        .on("click", centerState)
        .on("mouseover", d => handleHover(`state-${d.id}`))
        .on("mouseout", d => removeHover(`state-${d.id}`))
        .append('title').text(d => `Min: ${stateWaterQualData[d.id].min}, Max: ${stateWaterQualData[d.id].max}, Avg: ${stateWaterQualData[d.id].avg}`);
    };

    (topologyData && waterScoreData && stateWaterQualData) && translateData();
  }, [topologyData, waterScoreData, stateWaterQualData]);

  useEffect(() => {
    const addPoints = () => {
      if (areaInViewPort) {
        console.log(areaInViewPort.id);
        const facilities = stateFacilityObj.current[areaInViewPort.id];
        console.log(facilities);
        // todo: add facilities that have problems in areaInViewPort
        // todo: 11/11 Update - need to adjust the coords so the points appear on the map
        // todo: onClick, send to facility page on ECHO in new page using RegistryID
        // g.current.append('g')
        //   .attr('id', 'facilities')
        //   .selectAll('circle')
        //   .data(facilities)
        //   .enter()
        //   .append('circle')
        //   .attr('cx', (d) => d.areaCoords[0])
        //   .attr('cy', (d) => d.areaCoords[1])
        //   .on('click', (d) => reqRedirect(d))
        //   .attr('r', 8)
        //   .attr('fill', 'yellow')
        //   .attr('class', 'city-point')
        //   .append('title')
        //   .text((d) => d.areaName);
      }
      else {
        // g.current.select('#facilities')
        //   .remove();
      }
    };
    if (g.current)
      addPoints();
  }, [areaInViewPort]);

  return (<div className="map-container" ref={anchor} />);
};
