export interface Person {
  id: number;
  name: string;
  friends?: Person [];
  locationOn: boolean;
}
