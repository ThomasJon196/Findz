import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CurrentGroupService {
  groupName = "";

  setGroupName(groupName: string) {
    this.groupName = groupName;
  }
}
