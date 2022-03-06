import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson-client';
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

export const colorScale = [
  {color: '#CE0A05', test: (score, maxScore) => (maxScore - 10) < score},
  {color: '#FFAE43', test: (score, maxScore) => maxScore / 3 < score},
  {color: '#badee8', test: (score, maxScore) => maxScore / 10 < score},
  {color: noColor, test: R.T},
]

//this is the color scheme and scale
const colorFun = (maxScore, waterScore) => ({ id }) => {
  const score = waterScore.get(id);
  return R.prop('color', R.find(({ test }) => test(score, maxScore), colorScale))
};

// setting some boundaries
let x = width / 2;
let y = height / 2;
let k = 1;
const RADIUS = 4;

// this function's only goal is to keep the map rendered in the "view box"
export const MapRender = (props) => {
  const anchor = useRef();
  const {
    addCounty,
    areaInViewPort,
    centerState,
    facilitiesInViewPort,
    maxScore,
    setZoom,
    stateWaterQualData,
    topologyData,
    userLocation,
    usStates,
    waterScoreData,
    zoom,
  } = props;
  //refs, we don't want a rerender when these change!
  const svg = useRef(null);
  const g = useRef(null);

  // this hook builds the map and renders it
  useEffect(() => {
    const getMinMaxAvg = ({id}) => {
      const stateInfo = stateWaterQualData.find(({ fipsState }) => id === fipsState)
      return `Min: ${stateInfo?.min ?? 0}, Max: ${stateInfo?.max ?? 0}, Avg: ${stateInfo?.avg.toFixed(2) ?? 0}`
    }
    const translateData = () => {
      //set the svg to the anchor element
      d3.select(anchor.current).selectAll('*').remove();
      svg.current = d3.select(anchor.current).append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMin meet")
        .attr("height", "100%")
        .attr("width", "100%");

      //create an element d3 map
      const waterScore = d3.map();

      //go through each state in the  data and set the map
      for (let i = 0; i < waterScoreData.length; i += 1) {
        const countyWaterScore = waterScoreData[i];
        waterScore.set(countyWaterScore.fipsCounty, parseFloat(countyWaterScore.score).toFixed(2) * 100);
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
        .append('title').text(getMinMaxAvg);
    };

    (topologyData && waterScoreData && stateWaterQualData) && translateData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topologyData, waterScoreData, stateWaterQualData]);

  useEffect(() => {
    // todo: zoom to state when clicking on point
    // todo: lower z-index of point so you can click on counties and facilities
    if (userLocation && userLocation !== {}) {
      const coordinates = projection([userLocation.longitude, userLocation.latitude]);
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
  }, [userLocation])

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
      const circleRadius = RADIUS / k > 1 ? RADIUS / k : 1;
      g.current.selectAll('circle')
        .attr('r', circleRadius);
    } else {
      x = width / 2;
      y = height / 2;
      k = 1;
      g.current.select("#userLocation")
        .selectAll('circle')
        .attr('r', RADIUS);
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

  // this hook is triggered when the facilities are updated
  useEffect(() => {
    const addPoints = () => {
      // need to remove facilities from inactive states
      g.current.select('#facilities')
        .remove();
      if (facilitiesInViewPort.length) {
        const imbedCoordinates = R.converge(R.assoc('coordinates'), [R.compose(projection, R.props(['long', 'lat'])), R.identity])
        const facilities = R.o(R.filter(R.prop('coordinates')), R.map(imbedCoordinates))(facilitiesInViewPort);

        // redirect code is currently commented out
        g.current.append('g')
          .attr('id', 'facilities')
          .selectAll('circle')
          .data(facilities)
          .enter()
          .append('circle')
          .attr('cx', (d) => d.coordinates[0])
          .attr('cy', (d) => d.coordinates[1])
          .attr('r', RADIUS / k)
          .attr('fill', '#E15659')
          .attr('class', 'city-point')
          .append('title')
          .text((d) => d.facName);
      } else {
        setZoom(0.5);
      }
    };

    if (g.current) {
      addPoints();
    }
  }, [facilitiesInViewPort, setZoom]);

  return (<div className="map-container" ref={anchor} />);
};
