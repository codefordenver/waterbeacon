import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import * as R from 'ramda';
import { countyList } from '../utils/counties';
import './MapRender.css';

const width = 960;
const height = 600;
//create a path item
const path = d3.geoPath();

//change the following variable to adjust stroke width
const initSW = .5;
const noColor = '#FFFFFF';

// increases the border when hovering
const handleHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", 4 * initSW + "px");
};

// resets the border after hovering
const removeHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", initSW + "px");
};

const defaultScale = d3.geoAlbersUsa().scale();
const projection = d3.geoAlbersUsa()
  .translate([480, 300])
  .scale(defaultScale * 600 / 500);

//this is the color scheme and scale
const colorFun = (maxScore, waterScore) => ({ id }) => {
  const score = waterScore.get(id);
  if ((maxScore - 10) < score) {
    return '#CE0A05';
  }
  if (maxScore / 3 < score) {
    return '#FFAE43';
  }
  if (maxScore / 10 < score) {
    return '#badee8';
  }
  return noColor;
};

// setting some boundaries
let x = width / 2;
let y = height / 2;
let k = 1;

// this function's only goal is to keep the map rendered in the "view box"
export const MapRender = (props) => {
  const anchor = useRef();
  const { 
    topologyData,
    waterScoreData,
    stateWaterQualData,
    addCounty,
    maxScore,
    usStates,
    areaInViewPort,
    centerState,
    userLocation,
    setZoom,
    zoom,
  } = props;
  //refs, we don't want a rerender when these change!
  const svg = useRef(null);
  const g = useRef(null);

  // this hook builds the map and renders it
  useEffect(() => {
    const translateData = () => {
      //set the svg to the anchor element
      svg.current = d3.select(anchor.current).append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMin meet")
        .attr("height", "100%")
        .attr("width", "100%");

      //create an element d3 map
      const waterScore = d3.map();

      //go through each state in the unemploymentByState data and set the map
      for (let i = 0; i < waterScoreData.length; i += 1) {
        const countyWaterScore = waterScoreData[i];
        waterScore.set(countyWaterScore.fips_county_id, parseFloat(countyWaterScore.score).toFixed(2) * 100);
      };

      // returns a function that determines the color
      const color = colorFun(maxScore, waterScore);

      //this creates the data for the map
      const usCounties = topojson.feature(topologyData, topologyData.objects.counties);

      g.current = svg.current.append("g");
      //we append a new "g" element that will have all the county information
      g.current.append("g")
        //we set the class as "counties" for this element
        .attr("id", "counties")
        // with no path elements, the .data call will create them
        .selectAll("path")
        .data(usCounties.features)
        // enter goes into the recently selected elemnt
        .enter().append("path")
        .attr("d", path)
        .attr("id", d => `county-${d.id}`)
        // todo: make scores within .1 of maxScore #CE0A05
        .attr("fill", d => color(d))
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

      //todo: add timeline
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
        .on("click", d => {removeHover(`state-${d.id}`); centerState(d);})
        .on("mouseover", d => handleHover(`state-${d.id}`))
        .on("mouseout", d => removeHover(`state-${d.id}`))
        .append('title').text(d => `Min: ${stateWaterQualData[d.id].min}, Max: ${stateWaterQualData[d.id].max}, Avg: ${stateWaterQualData[d.id].avg}`);

      // todo: zoom to state when clicking on point
      // todo: lower z-index of point so you can click on counties and facilities
      if (userLocation !== {}) {
        const coordinates = projection([userLocation.long, userLocation.lat]);
        g.current.append('g')
          .attr('id', 'userLocation')
          .selectAll('circle')
          .data([userLocation])
          .enter()
          .append('circle')
          .attr('cx', () => coordinates[0])
          .attr('cy', () => coordinates[1])
          .attr('r', 8)
          .attr('fill', '#67bf5c')
          .attr("fill-opacity", "0.9")
          .attr('class', 'city-point')
          .append('title')
          .text(() => 'You Are Here');
      }
    };

    (topologyData && waterScoreData && stateWaterQualData) && translateData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topologyData, waterScoreData, stateWaterQualData]);

  const adjustViewPort = (aivp, zoom = 0.5) => {
    if (!g.current) return;
    //create variables for centering the state
    if (aivp) {
      var centroid = path.centroid(aivp);
      x = centroid[0];
      y = centroid[1];
      //calculate the zoom extent
      const boundsArr = path.bounds(aivp);
      const stateWidth = boundsArr[1][0] - boundsArr[0][0];
      const stateHeight = boundsArr[1][1] - boundsArr[0][1];
      const widthZoom = width / stateWidth;
      const heightZoom = height / stateHeight;
      k = zoom * Math.min(widthZoom, heightZoom);
      g.current.select("#userLocation")
        .selectAll('circle')
        .attr('r', 4);
    } else {
      x = width / 2;
      y = height / 2;
      k = 1;
      g.current.select("#userLocation")
        .selectAll('circle')
        .attr('r', 8);
    }
    g.current.select("#states")
      .selectAll('path')
      .attr("id", (d) => aivp && d === aivp ? `active` : `state-${d.id}`)
      .style('stroke', 'black')
      .style("stroke-width", `${initSW}px`);

    g.current.select('#active')
      .style('stroke', '#2d5e9e')
      .style("stroke-width", `${4 * initSW}px`);

    g.current.transition()
      .duration(750)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")");  
  };

  useEffect(() => {
    adjustViewPort(areaInViewPort, zoom);
  }, [areaInViewPort, zoom])

  // this hook is triggered when the user changes the zoom
  // it centers the map
  useEffect(() => {
    const addPoints = () => {
      // need to remove facilities from inactive states
      g.current.select('#facilities')
        .remove();
      if (areaInViewPort) {
        const facilitiesRaw = R.compose(R.flatten, R.pluck('facilities'), R.filter(R.propEq('fips_state_id', areaInViewPort.id)))(waterScoreData);
        const imbedCoordinates = R.converge(R.assoc('coordinates'), [R.compose(projection, R.props(['long', 'lat'])), R.identity])
        const facilities = R.map(imbedCoordinates, facilitiesRaw);

        // redirect code is currently commented out
        g.current.append('g')
          .attr('id', 'facilities')
          .selectAll('circle')
          .data(facilities)
          .enter()
          .append('circle')
          .attr('cx', (d) => d.coordinates[0])
          .attr('cy', (d) => d.coordinates[1])
          .attr('r', 2)
          .attr('fill', '#E15659')
          .attr('class', 'city-point')
          .append('title')
          .text((d) => d.FacName);
      } else {
        setZoom(0.5);
      }
    };

    if (g.current) {
      addPoints();
    }
  }, [areaInViewPort]);

  return (<div className="map-container" ref={anchor} />);
};
