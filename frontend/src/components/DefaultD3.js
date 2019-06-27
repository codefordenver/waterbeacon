import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';

import './utils/d3.css'

import * as unemploymentTsv from './tempData/unemployment.tsv';

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

const DefaultD3 = (props) => {
  const [topologyData, setTD] = useState(undefined);
  const [unemploymentData, setUD] = useState(undefined);
  //todo: use state unemployment data to add table on left
  const [stateUnemploymentData, setSUD] = useState(undefined);
  const anchor = useRef(null);
  const width = 960;
  const height = 600;

  //todo: create an element on the right that gives user map options
  useEffect(()=>{
    const getData = async () => {
      try {
        const topoLocation = "https://d3js.org/us-10m.v1.json";
        setTD(await d3.json(topoLocation))
    
        //todo: our data will come in with lat/long, hopefully;
        //todo: will need to use d3.geoContains(lat, long);
        const fipsData = await d3.tsv(unemploymentTsv);
        setUD(fipsData);

        let parsedStateInfo = stateFipsId;
        
        //for each fips specific data point, work on state data
        fipsData.forEach((fipsSpecific)=>{
          const stateId = fipsSpecific.id.substring(0,2);
          const stateData = parsedStateInfo[stateId];
          stateData.count = stateData.count ? stateData.count+1 : 1;
          stateData.max = stateData.max ? 
            Math.max(stateData.max, parseFloat(fipsSpecific.rate)) : 
            parseFloat(fipsSpecific.rate);
          stateData.min = stateData.min ? 
            Math.min(stateData.min, parseFloat(fipsSpecific.rate)) : 
            parseFloat(fipsSpecific.rate);
          stateData.avg = stateData.avg ? 
            ((stateData.avg*(stateData.count-1)+parseFloat(fipsSpecific.rate))/stateData.count).toFixed(2) : 
            parseFloat(fipsSpecific.rate);
            parsedStateInfo[stateId]=stateData;
        });
        setSUD(parsedStateInfo)
      } catch (error) {
        console.log('Error loading or parsing data.')
      }
    }
    (!topologyData && !unemploymentData) && getData();
  }, []);

  useEffect(()=> {
    const translateData = () => {
      //this variable will let us know if the map is centered on a state object
      let centered;

      //set the svg to the ancor element
      const svg = d3.select(anchor.current).append("svg")
        .attr("width", width)
        .attr("height", height);

      //create a path item
      const path = d3.geoPath();

      //create an element d3 map
      const unemployment = d3.map();
      
      //go through each state in the unemploymentByState data and set the map
      unemploymentData.forEach((countyUD)=>{
        unemployment.set(countyUD.id, +countyUD.rate);
      })

      //this is the color scheme
      //the range will need to be reset to be between 0 and 1 (or 0 and 100)
      //scheme color should change
      const color = d3.scaleThreshold().domain(d3.range(2, 10)).range(d3.schemeBlues[9]);
      
      //this creates the data for the map
      const usCounties = topojson.feature(topologyData, topologyData.objects.counties);

      const centerState = (d) => {
        //create variables for centering the state
        var x, y, k;

        if (d && centered !== d) {
          var centroid = path.centroid(d);
          console.log(centroid)
          x = centroid[0];
          y = centroid[1];
          //calculate the zoom extent
          const boundsArr = path.bounds(d);
          const stateWidth = boundsArr[1][0]-boundsArr[0][0];
          const stateHeight = boundsArr[1][1]-boundsArr[0][1];
          const widthZoom = width/stateWidth;
          const heightZoom = height/stateHeight;
          k=.8*Math.min(widthZoom, heightZoom);
          centered = d;
        } else {
          x = width / 2;
          y = height / 2;
          k = 1;
          centered = null;
        }
      
        g.select("#states")
          .selectAll("path")
          .classed("active", centered && function(d) { return d === centered; });
      
        g.transition()
          .duration(750)
          .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
          .style("stroke-width", 1.5 / k + "px");

        console.log(centered);
      }

      const g = svg.append("g")

      //we append a new "g" element that will have all the county information
      g.append("g")
        //we set the class as "counties" for this element
        .attr("id", "counties")
        //the following line selects all the "path" elements inside the new "g" element
        //hint: there are nome
        .selectAll("path")
        //have to convert this to the "features" array
        .data(usCounties.features)
        //enter goes into the recently selected elemnt
        //pressing append addes a new "path" element to match the length of the "features" array
        //that is why we had to use .data instead of .datum and convert it to an array
        .enter().append("path")
          //for each "path" that is created, we will set the "d" to the path
          .attr("d", path)
          //also, we will set the fill, which will give us our chloropleth
          .attr("fill", function(d) { return color(d.rate = unemployment.get(d.id)); })
          //we also want to create a new class for easy boundary editing in a style sheet
          .attr("class", "county-boundary")
          .append("title").text(function(d) {return d.rate + "%";})
          .attr("d", path);

      //can't use "mesh" because we want to create a zoom on state boundary function
      const usStates = topojson.feature(topologyData, topologyData.objects.states);
      
      //we append a new "g" element for the state boundaries
      g.append("g")
        //set the class
        .attr("id", "states")
        //select the "path" elements
        .selectAll("path")
        //give our new element the "data"
        .data(usStates.features)
        .enter().append("path")
          //create each state's individual path
          .attr("d", path)
          //give each path a boundary for easy coloring
          .attr("class", "state-boundary")
          //give a click listener for each state-boundary
          .on("click", centerState)
    }

    (topologyData && unemploymentData) && translateData();
  }, [topologyData, unemploymentData])

  if(!topologyData || !unemploymentData) {
    return null;
  }

  //todo: add options to view as state or county
  //todo: add rank on left sidebar

  return (
    <div ref={anchor} />
  )
}


export default DefaultD3;
