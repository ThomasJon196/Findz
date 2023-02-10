import {Group} from './group';
import {Person} from './person';

export const peter: Person = {id: 1, name: 'Peter', locationOn: true};
export const anna: Person = {id: 2, name: 'Anna', locationOn: false};
export const tobias: Person = {id: 3, name: 'Tobias', locationOn: true};

export const GROUPS: Group[] = [
  {id: 12, name: 'Karneval', members: [peter]},
  {id: 13, name: 'Geburtstag Tobi', members: [peter, tobias]},
  {id: 14, name: 'Feiern', members: [peter, anna, tobias]}
];
