import React, { useState, useRef } from 'react';
import Loader from 'react-loader-spinner';
import './utils/d3.css'

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';

// this component controls the logic that is shared between ChooseZoom and MapRender
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

  // this function adds counties to the table on left
  const addCounty = (d) => {
    const chosenOne = waterScoreData.find((county) => d.id === county.fips_county_id);

    return chosenOne && setCountyRanked(tempCR => tempCR.concat(chosenOne).sort((a,b) => b.score-a.score));
  };

  // when called, changes the area in viewport state, triggering useEffect function in map render
  const centerState = (d) => {
    //create variables for centering the state
    if (d && areaInViewPort !== d) {
      setAIVP(d);
    } else {
      setAIVP(null);
    }
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
        <small id="reset-zoom" onClick={() => setAIVP(null)}>Zoom to state, click on county to compare at left. Click here to reset.</small>
        <MapRender
          topologyData={topologyData}
          waterScoreData={waterScoreData}
          stateWaterQualData={stateWaterQualData}
          addCounty={addCounty}
          maxScore={maxScore}
          usStates={usStates}
          areaInViewPort={areaInViewPort}
          centerState={centerState}
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
