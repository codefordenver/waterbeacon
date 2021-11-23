import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import DefaultD3 from './DefaultD3';
import * as R from 'ramda';
import { getQuarterString } from '../utils/helpers';

// this component will retrieve the data from our database
const Retrieve = () => {
  // this is the data used to build the map
  const [topologyData, setTD] = useState(null);
  // this is the data used to color the map
  const [waterScoreData, setWaterScoreData] = useState(null);
  // this is the component that will hold the state information, along with min and max values
  const [stateWaterQualData, setStateWaterQualityData] = useState(null);

  const [quartersAvailable, setQuartersAvailable] = useState([]);
  const [quarterIndex, setQuarterIndex] = useState(0);
  const { quarter, year } = quartersAvailable[quarterIndex] ?? {}
  const chosenPeriod = getQuarterString({ quarter, year })

  const [userLocation, setUL] = useState({
    latitude: 39.734850,
    longitude:-104.995900
  });
  // holds the highest scoring three counties on initial render
  // data is sent to table on left pane
  // user can add and remove counties
  const [countiesRanked, setCountyRanked] = useState([]);
  // holds the max score for all counties
  const scoreList = R.pluck('score', countiesRanked);
  const maxScore = Math.max(...scoreList, 0) * 100;
  const [utilities, setUtilities] = useState([]);

  useEffect(() => {
    setUL({
      lat: 39.734850,
      long:-104.995900
    })
  }, []);

  useEffect(()=>{
    // retrieve topo data
    // can store topo data locally and import it
    const getTopoData = async () => {
      const topoLocation = "https://d3js.org/us-10m.v1.json";
      setTD(await d3.json(topoLocation));
      // uncomment following if loading topo data locally
      // setTD(topoLocation);
    }

    const getData = async () => {
      const { quarter: quarterSelection, year: yearSelection } = quartersAvailable[quarterIndex] ?? {}
      // calls the server set up as proxy in package.json to retrieve data
      const dataString = "/v1/data/?sources=locations,utilities&format=json";
      const quarterString = quarterSelection ? "&quarter=" + quarterSelection : "";
      const yearString = yearSelection ? "&year=" + yearSelection : "";
      const dataSRC = dataString + quarterString + yearString;
      const dataJSON = await fetch(dataSRC);
      const data = await dataJSON.json();
      data?.quarters && setQuartersAvailable(data?.quarters);
      data?.utilities && setUtilities(data?.utilities);
      data?.top_locations && setCountyRanked(data?.top_locations);
      data?.states && setStateWaterQualityData(data?.states);
      data?.locations && setWaterScoreData(data?.locations);
    }

    getTopoData();
    getData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [quarterIndex]);
 
  return (
    <DefaultD3
      topologyData={topologyData}
      waterScoreData={waterScoreData}
      stateWaterQualData={stateWaterQualData}
      maxScore={maxScore}
      countiesRanked={countiesRanked}
      quartersAvailable={quartersAvailable}
      updateChosenPeriod={setQuarterIndex}
      chosenPeriod={chosenPeriod}
      setCountyRanked={setCountyRanked}
      userLocation={userLocation}
      utilities={utilities}
    />
  )
}

export default Retrieve;
