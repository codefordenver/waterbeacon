import React, { useState, useRef, useMemo } from 'react';
import Loader from 'react-loader-spinner';
import './DefaultD3.css';
import * as R from 'ramda';

import { ChooseZoom } from './ChooseZoom';
import { MapRender } from './MapRender';
import { Table, Alert, Button, ButtonGroup } from 'react-bootstrap';
import Legend from './Legend';
import { getFacilities, getQuarterString } from '../utils/helpers';
import ewgLogo from '../../icons/ewg-logo.png';
import epaLogo from '../../icons/epa-logo.png';

// this component controls the logic that is shared between ChooseZoom and MapRender
const DefaultD3 = ({
  chosenPeriod,
  quartersAvailable,
  updateChosenPeriod,
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

  // this function adds counties to the table on left
  const addCounty = (d) => {
    const chosenOne = waterScoreData.find((county) => d.id === county.fipsCounty);
    setCC(chosenOne);

    return chosenOne && setCountyRanked(tempCR => {
      if (tempCR.find(({ fipsCounty }) => fipsCounty === d.id)) return tempCR;
      return tempCR.concat(chosenOne).sort((a,b) => a.score-b.score);
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

  const handleZoomOut = () => {
    if (zoom <= 0.5) {
      return setAIVP(null)
    }

    return setZoom(z => z/1.5 > 0.5 ? z/1.5 : 0.5)
  }

  if(!topologyData || !waterScoreData) return <div className="loader"><Loader type="Oval" color="#111111" height={80} width={80} /></div>

  //todo: make options class stay same width
  //todo: have CurrentSelection scroll when there are several counties
  return (
    <>
      <div className="map-content mt-4">
        <div className="options">
          {/*
          <ChooseZoom
            areaInViewPort={areaInViewPort}
            centerState={centerState}
            usStates={usStates}
            setAIVP={setAIVP}
          />*/
          }
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
          <div className="quarter-choice">
            {quartersAvailable.reverse().map((quarterOption = {}, index) => {
              const { quarter, year, existing } = quarterOption
              const value = getQuarterString({ quarter, year })
              const isCurrentSelection = chosenPeriod === value
              const variant = isCurrentSelection ? '' : 'outline-'
              const period = quartersAvailable.length - 1 - index;
              return (
                <Button
                  className={ 'rounded-0 mr-10'}
                  disabled={isCurrentSelection || !existing}
                  variant={variant + 'primary'}
                  onClick={() => updateChosenPeriod(period)}
                  key={value}
                >
                  {value}
                </Button>
              )
            })}
          </div>

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
              <Button onClick={() => setZoom(z => z*1.5)}>+</Button>
              <Button onClick={handleZoomOut}>-</Button>
            </ButtonGroup>
          )}
          <Legend />
        </div>
      </div>
    </>
  )
};

// todo: add facility's score
const CurrentSelection = ({ currentCounty, facilitiesInCounty, setCC }) => (
  <div className="selection-alert">
    <Alert dismissible variant="light" onClose={() => setCC(null)}>
      <Alert.Heading>{currentCounty.county}, {currentCounty.state}</Alert.Heading>
      <p>Closest Major City: {currentCounty.majorCity}</p>
      <p>Facilities in Violation</p>
      <ul style={{ textAlign:"left" }}>
        {facilitiesInCounty.map(facility => (
          <li key={facility.pwsId}>
            {facility.facName}:&nbsp;
            <a rel="noopener noreferrer" target="_blank" href={`https://echo.epa.gov/detailed-facility-report?fid=${facility.registryId}`}>
              <img className="logos" src={epaLogo} alt="EPA Link" />
            </a>
            &nbsp;-&nbsp;
            <a rel="noopener noreferrer" target="_blank" href={`https://www.ewg.org/tapwater/system.php?pws=${facility.pwsId}`}>
              <img className="logos" src={ewgLogo} alt="EWG Link" />
            </a>
          </li>
        ))}
      </ul>
    </Alert>
  </div>
);

const TopCounties = (props) => {
  const removeCounty = (index) => {
    props.setCountyRanked(R.remove(index, 1));
  };

  return (
    <Table striped bordered hover size="sm" className="county-list">
      <thead>
        <tr>
          <th>
            Rank
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
            <tr key={county.county + county.score}>
              <td>
                {county.rank}
              </td>
              <td className="county-selector" onClick={() => props.setCC(county)}>
                {county.county}
              </td>
              <td>
                {county.state}
              </td>
              <td style={{textAlign: "center"}}>
                {Math.floor(( 1 - county.score) * 100) + '%'}
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
