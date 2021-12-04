import * as R from 'ramda';

export const getFacilities = (id, utilities) => {
  if(!id) return [];
  const facilities = R.filter(R.propSatisfies(R.startsWith(id), 'fipsCode'), utilities);
  return facilities;
};

export const getQuarterString = ({ quarter, year }) => (
  `${quarter?.toUpperCase()}-${year}`
);
