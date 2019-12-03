import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import DefaultD3 from './DefaultD3';
import { countyList } from './utils/counties';

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

const Retrieve = (props) => {
  // !leave this
  const [topologyData, setTD] = useState(undefined);
  // !leave this
  const [waterScoreData, setWSD] = useState(undefined);
  // !leave this
  const [stateWaterQualData, setWQD] = useState(undefined);
  // !leave this
  const [countiesRanked, setCountyRanked] = useState([]);

  //start maxScore at 0, that way we will ensure a score is higher
  const maxScore = useRef(0);

  useEffect(()=>{
    const getTopoData = async () => {
      const topoLocation = "https://d3js.org/us-10m.v1.json";
      setTD(await d3.json(topoLocation));
    }

    const getLocations = async () => {
      if (localStorage.getItem('locData')) {
        const locData = localStorage.getItem('locData');
        return JSON.parse(locData);
      }
      const locationsSRC = "/v1/data/?sources=locations";
      const locJSON = await fetch(locationsSRC);
      const locData = await locJSON.json();
      localStorage.setItem('locData', JSON.stringify(locData));
      return locData;
    }

    const getData = async () => {
      const locData = await getLocations();
      console.log(locData);
      const { locations } = locData;
      const locCount = locations.length;
      const convLoc = Object.keys(countyList).map((countyId) => {
        for (let i = 0; i < locCount; i ++) {
          if (countyId === locations[i].fips_county_id) {
            return locations[i];
          }
        }
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
      
      let topCountyScores = [];
      //for each fips specific data point, work on state data
      locations.forEach((fipsSpecific)=>{
        // State FIPS ID is the first two characters of the county ID
        const stateId = fipsSpecific.fips_county_id.substring(0,2);
        const stateData = stateFipsId[stateId];
        stateData.count = stateData.count ? stateData.count+1 : 1;
        const currScore = parseFloat(fipsSpecific.score).toFixed(2)*100;
        stateData.max = stateData.max ? 
          Math.max(stateData.max, currScore) : 
          currScore;
        stateData.min = stateData.min ? 
          Math.min(stateData.min, currScore) : 
          currScore;
        currScore > maxScore.current && (maxScore.current = currScore);
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
    />
  )
}

export default Retrieve;
