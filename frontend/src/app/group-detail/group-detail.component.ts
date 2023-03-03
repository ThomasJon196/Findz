import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrls: ['./group-detail.component.scss']
})
export class GroupDetailComponent implements OnInit {

  //groups = GROUPS;
  //currentGroup?: Group;

  groupName: string = this.router.url.substring(16);
  groupMembers = [];

  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any>('/getGroupMembers?groupName=' + this.groupName)
      .subscribe(data => {
        console.log(data);
        this.groupMembers = data.memberlist;
      });
  }

  startAR() {
    this.http.get<any>('/webXR?groupname=' + this.groupName);
  }
}
