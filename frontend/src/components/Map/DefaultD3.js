import React, { useState, useRef, useMemo } from 'react';
import Loader from 'react-loader-spinner';
import './DefaultD3.css';
import * as R from 'ramda';

//import * as unemploymentTsv from './tempData/unemployment.tsv';
import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';
import { Table, Alert, Button, ButtonGroup } from 'react-bootstrap';
import ExpandIcon from '../../icons/ExpandIcon';
import Legend from './Legend';
import { getFacilities } from '../utils/helpers';

// this component controls the logic that is shared between ChooseZoom and MapRender
const DefaultD3 = ({
  topologyData,
  waterScoreData,
  setCountyRanked,
  countiesRanked,
  stateWaterQualData,
  maxScore,
  userLocation,
  utilities,
}) => {
  const [areaInViewPort, setAIVP] = useState(null);
  // todo: set first county as a "You are here"
  const [currentCounty, setCC] = useState(null)
  const [zoom, setZoom] = useState(0.5);
  const usStates = useRef(null);

  const facilitiesInViewPort = useMemo(() => {
    const currId = areaInViewPort?.id;
    return getFacilities(currId, utilities);
  }, [areaInViewPort, utilities]);

  const facilitiesInCounty = useMemo(() => {
    const currId = currentCounty?.fipsCounty;
    return getFacilities(currId, utilities);
  }, [currentCounty, utilities]);
  console.log(facilitiesInCounty);

  // this function adds counties to the table on left
  const addCounty = (d) => {
    const chosenOne = waterScoreData.find((county) => d.id === county.fipsCounty);
    setCC(chosenOne);

    return chosenOne && setCountyRanked(tempCR => {
      if (tempCR.find(({ fipsCounty }) => fipsCounty === d.id)) return tempCR;
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
                facilitiesInCounty={facilitiesInCounty}
                setCC={setCC}
              />
            }
          </div>
        </div>
      </div>
      <div className="map" >
        <MapRender
          addCounty={addCounty}
          areaInViewPort={areaInViewPort}
          centerState={centerState}
          facilitiesInViewPort={facilitiesInViewPort}
          maxScore={maxScore}
          setZoom={setZoom}
          stateWaterQualData={stateWaterQualData}
          topologyData={topologyData}
          userLocation={userLocation}
          usStates={usStates}
          waterScoreData={waterScoreData}
          zoom={zoom}
        />
        {areaInViewPort && (
          <ButtonGroup className="zoom-btn-grp" vertical>
            <Button onClick={() => setAIVP(null)} variant="danger" block><ExpandIcon /></Button>
            <Button onClick={() => setZoom(z => z*1.5)}>+</Button>
            <Button disabled={zoom <= 0.5} onClick={() => setZoom(z => z/1.5 > 0.5 ? z/1.5 : 0.5)}>-</Button>
          </ButtonGroup>
        )}
        <Legend />
      </div>
    </div>
  )
};

// todo: add facility's score
const CurrentSelection = ({ currentCounty, facilitiesInCounty, setCC }) => (
  <Alert dismissible variant="primary" onClose={() => setCC(null)}>
    <Alert.Heading>{currentCounty.county}, {currentCounty.state}</Alert.Heading>
    <p>Closest Major City: {currentCounty.majorCity}</p>
    <p>Facilities in Violation</p>
    <ul style={{ textAlign:"left" }}>
      {facilitiesInCounty.map(facility => (
        <li key={facility.pwsId}>
          <a rel="noopener noreferrer" target="_blank" href={`https://echo.epa.gov/detailed-facility-report?fid=${facility.registryId}`}>
            {facility.facName}
          </a>
        </li>
      ))}
    </ul>
  </Alert>
);

const TopCounties = (props) => {
  const removeCounty = (index) => {
    props.setCountyRanked(R.remove(index, 1));
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
