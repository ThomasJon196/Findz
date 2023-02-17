import {Group} from "./group";

export interface User {
  id: number;
  name: string;
  mail?: string;
  friends?: User [];
  groups?: Group[];
  locationOn: boolean;
}
