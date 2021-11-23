import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import DefaultD3 from './DefaultD3';
import * as R from 'ramda';

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
  const [topologyData, setTD] = useState(null);
  // this is the data used to color the map
  const [waterScoreData, setWSD] = useState(null);
  // this is the component that will hold the state information, along with min and max values
  const [stateWaterQualData, setWQD] = useState(null);
  const [quarter, setQuarter] = useState(null);
  const [year, setYear] = useState(null);
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
      // calls the server set up as proxy in package.json to retrieve data
      const dataString = "/v1/data/?sources=locations,utilities&format=json";
      const quarterString = quarter ? "&quarter=" + quarter : "";
      const yearString = year ? "&year=" + year : "";
      const dataSRC = dataString + quarterString + yearString;
      const dataJSON = await fetch(dataSRC);
      const data = await dataJSON.json();
      setUtilities(data?.utilities);
      if (data?.top_locations) {
        setCountyRanked(data.top_locations)
      }
      setWQD(data?.states);
      setWSD(data?.locations);
    }

    getTopoData();
    getData();
  }, [quarter, year]);
 
  return (
    <DefaultD3
      topologyData={topologyData}
      waterScoreData={waterScoreData}
      stateWaterQualData={stateWaterQualData}
      maxScore={maxScore}
      countiesRanked={countiesRanked}
      setCountyRanked={setCountyRanked}
      userLocation={userLocation}
      utilities={utilities}
    />
  )
}

export default Retrieve;
