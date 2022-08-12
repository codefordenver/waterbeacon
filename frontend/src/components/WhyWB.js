import React from 'react';
import { Image } from 'react-bootstrap';
import wbInfoLogo from '../images/infoWB.png'


export default function WhyWB() {
  return (
    <article id="why-wb" className="center-all">
      <div className="center-all">
        <h2 style={{ color: 'white'}}>Why Water Beacon?</h2>
        <Image src={wbInfoLogo} style={{ maxHeight: 100, padding:10 }}/>
      </div>
      <div className="center-all">
        <p>
             The vision of Water Beacon is to make drinking water quality data easy to understand.
        </p>
        <p>
            Using EPA data, we created score to identify which counties have good versus bad drinking water.
            Next, we use the score to rank each county. Counties ranked 1 have the best drinking water. The visualization is updated every quarter.
        </p>
        <p>
            In addition, we use Twitter to identify counties that may report water quality alerts. If you subscribe and submit your zipcode, you will
            recieve an notification if there are any water quality alerts within your county.
        </p>
        <p>
            Water Beacon is completly open-source. Click Github-Repo to view the source code
        </p>
      </div>
    </article>
  )
}
//
