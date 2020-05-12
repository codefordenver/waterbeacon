import React, { useState, useEffect } from 'react';
import { Typeahead } from 'react-bootstrap-typeahead';
import { Button } from 'react-bootstrap';
import './ChooseZoom.css';

export const stateList = [{id:"01", name:"ALABAMA"},{id:"02", name:"ALASKA"},
  {id:"04", name:"ARIZONA"},{id:"05", name:"ARKANSAS"},{id:"06", name:"CALIFORNIA"},
  {id:"08", name:"COLORADO"},{id:"09", name:"CONNECTICUT"},{id:"10", name:"DELAWARE"},
  {id:"11", name:"DISTRICT OF COLUMBIA"},{id:"12", name:"FLORIDA"},
  {id:"13", name:"GEORGIA"},{id:"15", name:"HAWAII"},{id:"16", name:"IDAHO"},
  {id:"17", name:"ILLINOIS"},{id:"18", name:"INDIANA"},{id:"19", name:"IOWA"},
  {id:"20", name:"KANSAS"},{id:"21", name:"KENTUCKY"},{id:"22", name:"LOUISIANA"},
  {id:"23", name:"MAINE"},{id:"24", name:"MARYLAND"},{id:"25", name:"MASSACHUSETTS"},
  {id:"26", name:"MICHIGAN"},{id:"27", name:"MINNESOTA"},{id:"28", name:"MISSISSIPPI"},
  {id:"29", name:"MISSOURI"},{id:"30", name:"MONTANA"},{id:"31", name:"NEBRASKA"},
  {id:"32", name:"NEVADA"},{id:"33", name:"NEW HAMPSHIRE"},{id:"34", name:"NEW JERSEY"},
  {id:"35", name:"NEW MEXICO"},{id:"36", name:"NEW YORK"},{id:"37", name:"NORTH CAROLINA"},
  {id:"38", name:"NORTH DAKOTA"},{id:"39", name:"OHIO"},{id:"40", name:"OKLAHOMA"},
  {id:"41", name:"OREGON"},{id:"42", name:"PENNSYLVANIA"},{id:"44", name:"RHODE ISLAND"},
  {id:"45", name:"SOUTH CAROLINA"},{id:"46", name:"SOUTH DAKOTA"},{id:"47", name:"TENNESSEE"},
  {id:"48", name:"TEXAS"},{id:"49", name:"UTAH"},{id:"50", name:"VERMONT"},
  {id:"51", name:"VIRGINIA"},{id:"53", name:"WASHINGTON"},{id:"54", name:"WEST VIRGINIA"},
  {id:"55", name:"WISCONSIN"},{id:"56", name:"WYOMING"}
];

export const ChooseZoom = ({ areaInViewPort, usStates, centerState, setAIVP }) => {
  const stateNames = stateList.map((state) => state.name);
  const [selected, setSel] = useState([]);

  useEffect(() => {
    const chooseState = () => {
      const stateIn = selected[0].toLowerCase();
      // get the fips ID of the state selected
      const { id } = stateList.find((state) => state.name.toLowerCase() === stateIn);
      // if the state searched for is already in the view box
      if (areaInViewPort && id === areaInViewPort.id) return null;
      // if the user chooses to view all states
      if (selected[0] === "All") {
        return centerState();
      };
      // find state in features
      const tempState = usStates.current.features.find((state) => state.id === id);
      // will call parent function to recenter view box
      tempState && centerState(tempState);
    }

    if (selected.length === 1) chooseState();
  }, [selected]);

  useEffect(() => {
    if (areaInViewPort) {
      const chosenStateName = stateList.find((state) => state.id === areaInViewPort.id).name;
      setSel([chosenStateName]);
    } else if (!areaInViewPort && selected.length === 1) {
      setSel([]);
    }
  }, [areaInViewPort])

  return (
    <div className="zoomer">
      <Typeahead
        id="choose-state"
        onChange={selected => setSel(selected)}
        options={stateNames}
        placeholder="Choose a state!"
        selected={selected}
      />
      <Button
        size="sm"
        variant="warning"
        disabled={selected.length === 0}
        onClick={() => setAIVP(null)}
      >
        Reset
      </Button>
    </div>
  )
};
