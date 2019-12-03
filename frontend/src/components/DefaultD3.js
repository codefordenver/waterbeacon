import React, { useState, useRef } from 'react';
import Loader from 'react-loader-spinner';
import './utils/d3.css'

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';

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
    if (d && areaInViewPort !== d) {
      setAIVP(d);
    } else {
      console.log('here');
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
        <small>Zoom to state, click on county to compare at left. Hit reset to zoom to bounds of U.S.</small>
        <MapRender
          topologyData={topologyData}
          waterScoreData={waterScoreData}
          stateWaterQualData={stateWaterQualData}
          addCounty={addCounty}
          maxScore={maxScore.current}
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
