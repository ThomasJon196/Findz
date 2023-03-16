import {Component, OnInit} from '@angular/core';

import {HttpClient} from "@angular/common/http";
import {LoginStatusService} from "../LoginStatusService";

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {
  groups = [];
  groupsAvailable: string = "dataNotLoaded";

  constructor(private http: HttpClient, public loginStatusService: LoginStatusService) {
    this.loginStatusService.setLoginStatus(true);
  }

  ngOnInit(): void {
    this.updateGroup();
  }

  updateGroup(): void {
    this.http.get<any>('/getGroups')
      .subscribe(data => {
        console.log(data);
        this.groups = data.grouplist;
        if (this.groups.length == 0) {
          this.groupsAvailable = "noGroupsAvailable";
        } else {
          this.groupsAvailable = "groupsAvailable";
        }
      });
  }
}
