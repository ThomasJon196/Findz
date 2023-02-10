import {Person} from "./person";

export interface Group {
  id: number;
  name: string;
  members: Person[];
}
