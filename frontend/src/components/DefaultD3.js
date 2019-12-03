import React, { useState, useRef } from 'react';
import Loader from 'react-loader-spinner';
import * as d3 from 'd3';
import './utils/d3.css'

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';

export const width = 960;
export const height = 600;
//create a path item
export const path = d3.geoPath();

//change the following variable to adjust stroke width
export const initSW = .5;

const DefaultD3 = ({
  topologyData,
  waterScoreData,
  setCountyRanked,
  countiesRanked,
  stateWaterQualData,
  maxScore,
}) => {
  const [areaInViewPort, setAIVP] = useState(null);
  const usStates = useRef(null);
  const centered = useRef(null);
  //refs, we don't want a rerender when these change!
  const g = useRef(null);

  // setting some boundaries
  let x = width / 2;
  let y = height / 2;
  let k = 1;

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
  };

  const centerState = (d) => {
    //create variables for centering the state
    if (d && centered.current !== d) {
      var centroid = path.current.centroid(d);
      x = centroid[0];
      y = centroid[1];
      //calculate the zoom extent
      const boundsArr = path.current.bounds(d);
      const stateWidth = boundsArr[1][0] - boundsArr[0][0];
      const stateHeight = boundsArr[1][1] - boundsArr[0][1];
      const widthZoom = width / stateWidth;
      const heightZoom = height / stateHeight;
      k = .5 * Math.min(widthZoom, heightZoom);
      centered.current = d;
    }
    else {
      x = width / 2;
      y = height / 2;
      k = 1;
      centered.current = null;
    }
    g.current.select("#states")
      .selectAll("path")
      .classed("active", centered.current && function (d) { return d === centered.current; });
    g.current.selectAll("#active")
      .style("stroke-width", k * initSW + "px")
      .style("stroke", "#2d5e9e")
      .attr("fill", "none");
    g.current.transition()
      .duration(750)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")");
    setAIVP(centered.current);
  };

  if(!topologyData || !waterScoreData ) return <Loader type="Oval" color="#111111" height={80} width={80} className="loader" />

  // todo: make the ChooseZoom component work; manage AIVP state here
  // todo: add populace areas along the bottom
  return (
    <div className="map-content">
      <div className="options">
        <ChooseZoom
          areaInViewPort={areaInViewPort}
          centerState={centerState}
          usStates={usStates}
        />
        <TopCounties countiesRanked={countiesRanked} setCountyRanked={setCountyRanked} />
      </div>
      <div className="map" >
        <small>Zoom to state, click on county to compare at left. Hit reset to zoom to bounds of U.S.</small>
        <MapRender
          topologyData={topologyData}
          waterScoreData={waterScoreData}
          g={g}
          stateWaterQualData={stateWaterQualData}
          centerState={centerState}
          addCounty={addCounty}
          maxScore={maxScore.current}
          usStates={usStates}
          areaInViewPort={areaInViewPort}
        />
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
