import React, { useState, useEffect } from 'react';
import { stateList } from './DefaultD3';
export const ChooseZoom = (props) => {
  //todo: crawl environmental working group and add utilities
  const [states, setStates] = useState(stateList[0].name);
  const callCenter = (event) => {
    const tempState = event.target.value;
    setStates(tempState);
    if (tempState === "NONE") {
      return props.centerState();
    };
    let id;
    stateList.forEach((state) => {
      if (state.name === tempState) {id = state.id;};
    });
    if (!props.areaInViewPort) { }
    else if (id === props.areaInViewPort.id) {return null;};
    props.usStates.current.features.forEach((state) => {
      if (state.id === id) {
        props.centerState(state);
        return null;
      };
    });
  };
  useEffect(() => {
    const setStateInView = () => {
      stateList.forEach((state) => {
        props.areaInViewPort.id === state.id && (setStates(state.name));
      });
    };
    props.areaInViewPort ? setStateInView() : setStates(stateList[0].name);
  }, [props.areaInViewPort]);
  return (<form className="zoomer zoom-form" onSubmit={callCenter}>
    <div className="col-sm-9">
      <div className="zoom-row form-row">
        <div className="col-sm-3">
          <div className="form-label">
            State
            </div>
        </div>
        <div className="col-sm-9">
          <select className="form-control" value={states} onChange={callCenter}>
            {stateList.map((state) => { return (<option key={state.id}>{state.name}</option>); })}
          </select>
        </div>
      </div>
    </div>
    <div className="col-sm-3">
      <div className="group btn-group">
        <button className="btn btn-outline-info" disabled={!props.areaInViewPort} onClick={() => props.centerState()}>
          Reset
        </button>
      </div>
    </div>
  </form>);
};
