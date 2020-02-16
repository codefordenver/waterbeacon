import React, { useState, useRef } from 'react';
import Loader from 'react-loader-spinner';
import './utils/d3.css'

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';
import { Table } from 'react-bootstrap';

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

  return (
    <div className="map-content">
      <div className="options">
        <ChooseZoom
          areaInViewPort={areaInViewPort}
          centerState={centerState}
          usStates={usStates}
          setAIVP={setAIVP}
        />
        <TopCounties
          countiesRanked={countiesRanked}
          setCountyRanked={setCountyRanked}
        />
      </div>
      <div className="map" >
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
    <Table striped bordered hover variant="dark" size="sm" className="county-list">
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
            <tr key={county.county}>
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
    </Table>
  )
}

export default DefaultD3;
