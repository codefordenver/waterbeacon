import React, { useState, useEffect } from 'react';
import { stateList } from './DefaultD3';
import './ChooseZoom.css';

export const ChooseZoom = (props) => {
  const [states, setStates] = useState(stateList[0].name);
  const [viewToggle, setVT] = useState(false);

  useEffect(() => {
    const centerState = () => {
      const { id } = stateList.find((state) => state.name === states);
      if (!props.areaInViewPort || id === props.areaInViewPort.id) return null;
      if (states === "All") {
        return props.centerState();
      };
      const tempState = props.usStates.current.features.find((state) => state.id === id);
      tempState && props.centerState(tempState);
    }

    if (viewToggle) setVT(false);
    centerState();
  }, [states])

  useEffect(() => {
    const setStateInView = () => {
      const { name } = stateList.find((state) => props.areaInViewPort.id === state.id );
      setStates(name);
    };
    props.areaInViewPort ? setStateInView() : setStates(stateList[0].name);
  }, [props.areaInViewPort]);

  // todo: make drop-down look like this: https://codepen.io/miniven/pen/ZJydge
  return (
  <div className="zoomer zoom-form">
    <div className="col-sm-9 zoom-choice">
      <div className="selector-toggle" onClick={() => setVT(!viewToggle)}>
        <div className="col-sm-9">{states}</div>
        <div className="col-sm-3">X</div>
      </div>
      <div className="selector-list">
        {viewToggle && stateList.map((state) => <div key={`selector-${state.id}`} className="col-sm-9" onClick={() => setStates(state.name)}>{state.name}</div>)}
      </div>
    </div>
    <div className="col-sm-3">
      <div className="group btn-group">
        <button className="btn btn-outline-info" disabled={!props.areaInViewPort} onClick={() => props.centerState()}>
          Reset
        </button>
      </div>
    </div>
  </div>);
};
