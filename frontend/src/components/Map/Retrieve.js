import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import DefaultD3 from './DefaultD3';
import { countyList } from '../utils/counties';

const stateFipsId = {
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

// this component will retrieve the data from our database
const Retrieve = () => {
  // this is the data used to build the map
  const [topologyData, setTD] = useState(undefined);
  // this is the data used to color the map
  const [waterScoreData, setWSD] = useState(undefined);
  // this is the component that will hold the state information, along with min and max values
  const [stateWaterQualData, setWQD] = useState(undefined);
  const [userLocation, setUL] = useState({
    latitude: 39.734850,
    longitude:-104.995900
  });
  // holds the highest scoring three counties on initial render
  // data is sent to table on left pane
  // user can add and remove counties 
  const [countiesRanked, setCountyRanked] = useState([]);
  // holds the max score for all counties
  const [maxScore, setMax] = useState(0);

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

    const getLocations = async () => {
      // stores the location data in session storage
      // speeds up rerenders in development
      if (sessionStorage.getItem('locData')) {
        const locData = sessionStorage.getItem('locData');
        return JSON.parse(locData);
      }
      // calls the server set up as proxy in package.json to retrieve data
      const locationsSRC = "/v1/data/?sources=locations";
      const locJSON = await fetch(locationsSRC);
      const locData = await locJSON.json();
      // stores data retrieved in browser
      sessionStorage.setItem('locData', JSON.stringify(locData));
      return locData;
    }

    const getData = async () => {
      const locData = await getLocations();
      const { locations } = locData;
      const locCount = locations.length;
      const convLoc = Object.keys(countyList).map((countyId) => {
        // could do an array find here, but there is potential that no county is returned
        // when there is no county returned, it will trigger error
        for (let i = 0; i < locCount; i ++) {
          if (countyId === locations[i].fips_county_id) {
            return locations[i];
          }
        }

        // if a county is not in our db, will need to establish data for the county
        const county = countyList[countyId];
        return {
          county: county.Name,
          fips_county_id: countyId,
          fips_state_id: countyId.substring(0, 2),
          score: 0,
          facilities: [],
        }
      })
      setWSD(convLoc);
      
      // two variables to hold data until we are ready to set state
      let topCountyScores = [];
      let tempMaxScore = 0
      //for each fips specific data point, work on state data
      locations.forEach((fipsSpecific)=>{
        // State FIPS ID is the first two characters of the county ID
        const stateId = fipsSpecific.fips_state_id;
        const stateData = stateFipsId[stateId];
        stateData.count = stateData.count ? stateData.count + 1 : 1;
        // only need to go two spots past decimal
        const currScore = parseFloat(fipsSpecific.score).toFixed(2)*100;
        // test to find the max county score for a state
        stateData.max = stateData.max ? 
          Math.max(stateData.max, currScore) : 
          currScore;
        // test to find the min county score for a state
        stateData.min = stateData.min ? 
          Math.min(stateData.min, currScore) : 
          currScore;
        // reset the tempMaxScore if currScore is larger
        currScore > tempMaxScore && (tempMaxScore = currScore);

        // build the three-county table
        if(topCountyScores.length<3) {
          topCountyScores.push(fipsSpecific)
        } else {
          topCountyScores.push(fipsSpecific);
          topCountyScores.sort((a,b) => b.score-a.score)
          topCountyScores.pop();
        }
        //!: average is not actually average
        //!: does not account for population
        stateData.avg = stateData.avg ? 
          ((stateData.avg*(stateData.count-1)+currScore)/stateData.count).toFixed(2) : 
          currScore;
        stateFipsId[stateId]=stateData;
      });
      setMax(tempMaxScore);
      setCountyRanked(topCountyScores);
      setWQD(stateFipsId);
    };

    if (!topologyData) getTopoData();

    if (!waterScoreData) getData();
  }, []);
  
  return (
    <DefaultD3
      topologyData={topologyData}
      waterScoreData={waterScoreData}
      stateWaterQualData={stateWaterQualData}
      maxScore={maxScore}
      countiesRanked={countiesRanked}
      setCountyRanked={setCountyRanked}
      userLocation={userLocation}
    />
  )
}

export default Retrieve;
