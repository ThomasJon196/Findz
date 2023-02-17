import {Group} from './group';
import {User} from './User';

export const peter: User = {id: 1, name: 'Peter', locationOn: true};
export const anna: User = {id: 2, name: 'Anna', locationOn: false};
export const tobias: User = {id: 3, name: 'Tobias', locationOn: true};

export const GROUPS: Group[] = [
  {id: 12, name: 'Karneval', members: [peter]},
  {id: 13, name: 'Geburtstag Tobi', members: [peter, tobias]},
  {id: 14, name: 'Feiern', members: [peter, anna, tobias]}
];

