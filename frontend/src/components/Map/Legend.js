import React, { useState } from 'react';
import Minimize from '../../icons/Minimize'
import * as R from 'ramda';
import { colorScale } from './MapRender';

const maxScore = 100;
const scoreRange = [10, 30, 50, 95];
const getColor = (score, maxScore) => {
  return R.o(R.prop('color'), R.find(({ test }) => test(score, maxScore)))(colorScale);
};

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
          <p>You Are Here</p>
          <svg width="14px" height="14px">
            <circle cx="7" cy="7" fill="#67bf5c" r="7"/>
          </svg>
          <svg className="gradient" width={scoreRange.length * 20} height={14}>
            {scoreRange.map((score, index) => <rect key={`legend${score}`} width={20} height={14} fill={getColor(score, maxScore)} x={ 20 * index }/>)}
          </svg>
          <div className="gradient words">
            <span>Low Score</span>
            <span>High Score</span>
          </div>
        </>
      )}
    </div>
  )
};

export default Legend;
