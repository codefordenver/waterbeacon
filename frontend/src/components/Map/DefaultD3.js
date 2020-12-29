import React, { useState, useRef, useEffect } from 'react';
import Loader from 'react-loader-spinner';
import './DefaultD3.css';

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';
import { Table, Alert, Button, ButtonGroup } from 'react-bootstrap';

// this component controls the logic that is shared between ChooseZoom and MapRender
const DefaultD3 = ({
  topologyData,
  waterScoreData,
  setCountyRanked,
  countiesRanked,
  stateWaterQualData,
  maxScore,
  userLocation
}) => {
  const [areaInViewPort, setAIVP] = useState(null);
  // todo: set first county as a "You are here"
  const [currentCounty, setCC] = useState(null)
  const [zoom, setZoom] = useState(0.5);
  const usStates = useRef(null);

  // this function adds counties to the table on left
  const addCounty = (d) => {
    const chosenOne = waterScoreData.find((county) => d.id === county.fips_county_id);
    setCC(chosenOne);

    return chosenOne && setCountyRanked(tempCR => {
      if (tempCR.find(({ fips_county_id }) => fips_county_id === d.id)) return tempCR;
      return tempCR.concat(chosenOne).sort((a,b) => b.score-a.score);
    });
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

  if(!topologyData || !waterScoreData) return <div className="loader"><Loader type="Oval" color="#111111" height={80} width={80} /></div>

  //todo: make options class stay same width
  //todo: have CurrentSelection scroll when there are several counties
  return (
    <div className="map-content">
      <div className="options">
        <ChooseZoom
          areaInViewPort={areaInViewPort}
          centerState={centerState}
          usStates={usStates}
          setAIVP={setAIVP}
        />
        <div className="info-panel">
          <div className="info">
            <TopCounties
              countiesRanked={countiesRanked}
              setCountyRanked={setCountyRanked}
              setCC={setCC}
            />
          </div>
          <div className="info">
            {currentCounty &&
              <CurrentSelection
                currentCounty={currentCounty}
                setCC={setCC}
              />
            }
          </div>
        </div>
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
          setZoom={setZoom}
          zoom={zoom}
          userLocation={userLocation}
        />
        {areaInViewPort && (
          <ButtonGroup className="zoom-btn-grp" vertical>
            <Button onClick={() => setZoom(z => z*1.5)}>+</Button>
            <Button disabled={zoom <= 0.5} onClick={() => setZoom(z => z/1.5 > 0.5 ? z/1.5 : 0.5)}>-</Button>
          </ButtonGroup>
        )}
      </div>
    </div>
  )
};

// todo: add facility's score
const CurrentSelection = ({ currentCounty, setCC }) => (
  <Alert dismissible variant="primary" onClose={() => setCC(null)}>
    <Alert.Heading>{currentCounty.county}, {currentCounty.state}</Alert.Heading>
    <p>Closest Major City: {currentCounty.major_city}</p>
    <p>Facilities in Violation</p>
    <ul style={{textAlign:"left"}}>
      {currentCounty.facilities.map(facility => (
        <li key={facility.PWSId}>{facility.FacName}</li>
      ))}
    </ul>
  </Alert>
);

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
              <td className="county-selector" onClick={() => props.setCC(county)}>
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
