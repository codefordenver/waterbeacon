import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import Loader from 'react-loader-spinner';

import './utils/d3.css'

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { countyList } from './utils/counties';

export const stateFipsId = {
  "56":{State:"WY",},"54":{State:"WV",},"55":{State:"WI",},
  "53":{State:"WA",},"50":{State:"VT",},"78":{State:"VI",},
  "51":{State:"VA",},"49":{State:"UT",},"74":{State:"UM",},
  "48":{State:"TX",},"47":{State:"TN",},"46":{State:"SD",},
  "45":{State:"SC",},"44":{State:"RI",},"70":{State:"PW",},
  "72":{State:"PR",},"42":{State:"PA",},"41":{State:"OR",},
  "40":{State:"OK",},"39":{State:"OH",},"36":{State:"NY",},
  "32":{State:"NV",},"35":{State:"NM",},"34":{State:"NJ",},
  "33":{State:"NH",},"31":{State:"NE",},"38":{State:"ND",},
  "37":{State:"NC",},"30":{State:"MT",},"28":{State:"MS",},
  "69":{State:"MP",},"29":{State:"MO",},"27":{State:"MN",},
  "26":{State:"MI",},"68":{State:"MH",},"23":{State:"ME",},
  "24":{State:"MD",},"25":{State:"MA",},"22":{State:"LA",},
  "21":{State:"KY",},"20":{State:"KS",},"18":{State:"IN",},
  "17":{State:"IL",},"16":{State:"ID",},"19":{State:"IA",},
  "15":{State:"HI",},"66":{State:"GU",},"13":{State:"GA",},
  "64":{State:"FM",},"12":{State:"FL",},"10":{State:"DE",},
  "11":{State:"DC",},"09":{State:"CT",},"08":{State:"CO",},
  "06":{State:"CA",},"04":{State:"AZ",},"60":{State:"AS",},
  "05":{State:"AR",},"01":{State:"AL",},"02":{State:"AK",}
};

export const stateList = [{id:"NA", name: "All"},{id:"01", name:"ALABAMA"},{id:"02", name:"ALASKA"},
  {id:"04", name:"ARIZONA"},{id:"05", name:"ARKANSAS"},{id:"06", name:"CALIFORNIA"},
  {id:"08", name:"COLORADO"},{id:"09", name:"CONNECTICUT"},{id:"10", name:"DELAWARE"},
  {id:"11", name:"DISTRICT OF COLUMBIA"},{id:"12", name:"FLORIDA"},
  {id:"13", name:"GEORGIA"},{id:"15", name:"HAWAII"},{id:"16", name:"IDAHO"},
  {id:"17", name:"ILLINOIS"},{id:"18", name:"INDIANA"},{id:"19", name:"IOWA"},
  {id:"20", name:"KANSAS"},{id:"21", name:"KENTUCKY"},{id:"22", name:"LOUISIANA"},
  {id:"23", name:"MAINE"},{id:"24", name:"MARYLAND"},{id:"25", name:"MASSACHUSETTS"},
  {id:"26", name:"MICHIGAN"},{id:"27", name:"MINNESOTA"},{id:"28", name:"MISSISSIPPI"},
  {id:"29", name:"MISSOURI"},{id:"30", name:"MONTANA"},{id:"31", name:"NEBRASKA"},
  {id:"32", name:"NEVADA"},{id:"33", name:"NEW HAMPSHIRE"},{id:"34", name:"NEW JERSEY"},
  {id:"35", name:"NEW MEXICO"},{id:"36", name:"NEW YORK"},{id:"37", name:"NORTH CAROLINA"},
  {id:"38", name:"NORTH DAKOTA"},{id:"39", name:"OHIO"},{id:"40", name:"OKLAHOMA"},
  {id:"41", name:"OREGON"},{id:"42", name:"PENNSYLVANIA"},{id:"44", name:"RHODE ISLAND"},
  {id:"45", name:"SOUTH CAROLINA"},{id:"46", name:"SOUTH DAKOTA"},{id:"47", name:"TENNESSEE"},
  {id:"48", name:"TEXAS"},{id:"49", name:"UTAH"},{id:"50", name:"VERMONT"},
  {id:"51", name:"VIRGINIA"},{id:"53", name:"WASHINGTON"},{id:"54", name:"WEST VIRGINIA"},
  {id:"55", name:"WISCONSIN"},{id:"56", name:"WYOMING"}
];

const colorScale = (maxScore) => {
  const iteration = 10;
  const csStart = '#e1f5fe';
  const csEnd = '#01579b';
  const colorScale = d3.quantize(d3.interpolateHcl(csStart,csEnd), iteration);
  return d3.scaleThreshold().domain(d3.range(0,maxScore, maxScore/(iteration+1)))
    .range(colorScale);
};

//change the following variable to adjust stroke width
const initSW = .5;

const handleHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", 4 * initSW + "px");
};

const removeHover = (identifier) => {
  d3.select(`#${identifier}`)
    .style("stroke-width", initSW + "px");
}

const DefaultD3 = () => {
  const [topologyData, setTD] = useState(undefined);
  const [waterScoreData, setWSD] = useState(undefined);
  //todo: use state unemployment data to add table on left
  const [stateWaterQualData, setWQD] = useState(undefined);

  const [countiesRanked, setCountyRanked] = useState([]);

  //this will not change.
  const anchor = useRef(null);

  //refs, we don't want a rerender when these change!
  const svg = useRef(null);
  const g = useRef(null);
  const centered = useRef(null);
  const usStates = useRef(null);
  const usCounties = useRef(null);
  
  //start maxScore at 0, that way we will ensure a score is higher
  const maxScore = useRef(0);

  //we want to pass this to child components
  //want it to send new value when updated
  const [areaInViewPort, setAIVP] = useState(undefined);

  //create a path item
  const path = useRef(d3.geoPath());

  // setting some boundaries
  const width = 960;
  const height = 600;
  let x = width/2;
  let y = height/2;
  let k = 1;

  const centerState = (d) => {
    //create variables for centering the state
    if (d && centered !== d) {
      var centroid = path.current.centroid(d);
      x = centroid[0];
      y = centroid[1];
      //calculate the zoom extent
      const boundsArr = path.current.bounds(d);
      const stateWidth = boundsArr[1][0]-boundsArr[0][0];
      const stateHeight = boundsArr[1][1]-boundsArr[0][1];
      const widthZoom = width/stateWidth;
      const heightZoom = height/stateHeight;
      k=.5*Math.min(widthZoom, heightZoom);
      centered.current = d;
    } else {
      x = width / 2;
      y = height / 2;
      k = 1;
      centered.current = null;
    }
  
    //todo: double check this
    g.current.select("#states")
      .selectAll("path")
      .classed("active", centered.current && function(d) { return d === centered.current; })

    g.current.selectAll("#active")
      .style("stroke-width", k*initSW + "px")
      .style("stroke", "#2d5e9e")
      .attr("fill", "none")

    g.current.transition()
      .duration(750)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")

    setAIVP(centered.current);
  }

  const addCounty = (d) => {
    const getCounty = () => {
      const counties = waterScoreData.length;
      for(let i = 0; i<=counties; i++){
        const county = waterScoreData[i];
        if(county){
          if(d.id===county.fips_county_id){
            return county;
          }
        }
      }
    }
    const chosenOne = getCounty();

    return chosenOne && setCountyRanked(tempCR => tempCR.concat(chosenOne).sort((a,b) => b.score-a.score));
  }

  useEffect(()=>{
    const getData = async () => {
      try {
        const topoLocation = "https://d3js.org/us-10m.v1.json";
        setTD(await d3.json(topoLocation));

        const locationsLocation = "/v1/data/?sources=locations";
        const locJSON = await fetch(locationsLocation);
        const locData = await locJSON.json();
        const locations = locData.locations;
        setWSD(locations);

        let parsedStateInfo = stateFipsId;
        
        let countyList = [];
        //for each fips specific data point, work on state data
        locations.forEach((fipsSpecific)=>{
          const stateId = fipsSpecific.fips_county_id.substring(0,2);
          const stateData = parsedStateInfo[stateId];
          stateData.count = stateData.count ? stateData.count+1 : 1;
          const currScore = parseFloat(fipsSpecific.score).toFixed(2)*100;
          stateData.max = stateData.max ? 
            Math.max(stateData.max, currScore) : 
            currScore;
          stateData.min = stateData.min ? 
            Math.min(stateData.min, currScore) : 
            currScore;
          currScore>maxScore.current && (maxScore.current = currScore);
          if(countyList.length<3) {
            countyList.push(fipsSpecific)
          }else {
            countyList.push(fipsSpecific);
            countyList.sort((a,b) => b.score-a.score)
            countyList.pop();
          }
          //!: average is not actually average
          //!: does not account for population
          stateData.avg = stateData.avg ? 
            ((stateData.avg*(stateData.count-1)+currScore)/stateData.count).toFixed(2) : 
            currScore;
            parsedStateInfo[stateId]=stateData;
        });
        setCountyRanked(countyList);
        setWQD(parsedStateInfo);
      } catch (error) {
        console.log('Error loading or parsing data.');
      }
    }
    (!topologyData && !waterScoreData) && getData();
  }, []);

  useEffect(()=> {
    const translateData = () => {
      //set the svg to the anchor element
      svg.current = d3.select(anchor.current).append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`);

      //create an element d3 map
      const waterScore = d3.map();
      //go through each state in the unemploymentByState data and set the map
      waterScoreData.forEach((countyWaterScore)=>{
        waterScore.set(countyWaterScore.fips_county_id, +parseFloat(countyWaterScore.score).toFixed(2)*100);
      });

      //this is the color scheme and scale
      const noColor = 'rgb(248,249,250)';
      const color = colorScale(maxScore.current);
      
      //this creates the data for the map
      usCounties.current = topojson.feature(topologyData, topologyData.objects.counties);

      g.current = svg.current.append("g")

      //we append a new "g" element that will have all the county information
      g.current.append("g")
        //we set the class as "counties" for this element
        .attr("id", "counties")
        // with no path elements, the .data call will create them
        .selectAll("path")
        .data(usCounties.current.features)
        // enter goes into the recently selected elemnt
        .enter().append("path")
          .attr("d", path.current)
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
          .append("title").text(d => (countyList[d.id] ? countyList[d.id].Name : "Unknown") + ": " + d.score + "%");

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
          .attr("d", path.current)
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
      //todo: add icons from noun project as water utilities
    }

    (topologyData && waterScoreData && stateWaterQualData) && translateData();
  }, [topologyData, waterScoreData, stateWaterQualData])


  if(!topologyData || !waterScoreData ) return <Loader type="Oval" color="#somecolor" height={80} width={80} className="loader" />

  //todo: add populace areas along the bottom
  return (
    <div className="map-content">
      <TopCounties countiesRanked={countiesRanked} setCountyRanked={setCountyRanked} />
      <div className="map" >
        <ChooseZoom areaInViewPort={areaInViewPort} centerState={centerState} usStates={usStates}/>
        <small>Zoom to state, click on county to compare at left. Hit reset to zoom to bounds of U.S.</small>
        <div className="map-container" ref={anchor} />
      </div>
    </div>
  )
};

const TopCounties = (props) => {
  const removeCounty = (index) => {
    const tempCountyA = props.countiesRanked.slice(0,index);
    const tempCountyB = props.countiesRanked.slice(index+1);
    const tempCounty = tempCountyA.concat(tempCountyB);
    props.setCountyRanked(tempCounty);
  };

  return (
    <table className="county-list">
      <thead>
        <tr>
          <th>
            Number
          </th>
          <th>
            County
          </th>
          <th>
            State
          </th>
          <th>
            Rating
          </th>
          <th>
            Remove
          </th>
        </tr>
      </thead>
      <tbody>
        {props.countiesRanked.map((county, index)=>{
          return (
            <tr key={index}>
              <td>
                {index+1}
              </td>
              <td>
                {county.county}
              </td>
              <td>
                {county.state}
              </td>
              <td>
                {county.score}
              </td>
              <td className="remove-county" onClick={()=>removeCounty(index)}>
                X
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

export default DefaultD3;
