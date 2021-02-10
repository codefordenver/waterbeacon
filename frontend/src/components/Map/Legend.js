import React, { useState } from 'react';
import Minimize from '../../icons/Minimize'
import * as R from 'ramda';
import { Button } from 'react-bootstrap';

const Legend = () => {
  const [showLegend, setShowLegend] = useState(true);

  return (
    <div className="legend">
      <p>Legend</p>
      <Minimize id="minimize_legend" onClick={() => setShowLegend(R.not)} width="14px" />
      {showLegend && (
        <>
          <p>Facility in Violation</p>
          <svg width="14px" height="14px">
            <circle cx="7" cy="7" fill="red" r="7"/>
          </svg>
        </>
      )}
    </div>
  )
};

export default Legend;
