import {Component, OnInit} from '@angular/core';

import {HttpClient} from "@angular/common/http";
import {LoginStatusService} from "../LoginStatusService";
import {CurrentGroupService} from "../CurrentGroupService";

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {
  groups = ["hallo"];

  constructor(private http: HttpClient, public loginStatusService: LoginStatusService, public currentGroupService: CurrentGroupService) {
    this.loginStatusService.setLoginStatus(true);
  }

  ngOnInit(): void {
    this.updateGroup();
  }

  updateGroup(): void {
    this.http.get<any>('/getGroups')
      .subscribe(data => {
        console.log(data);
        //this.groups = data.grouplist;
      });
  }

  updateCurrentGroup(groupName: string) {
    //this.currentGroupService.setGroupName(groupName);
  }
}
