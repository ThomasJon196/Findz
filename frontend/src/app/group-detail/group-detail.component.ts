import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrls: ['./group-detail.component.scss']
})
export class GroupDetailComponent implements OnInit {

  groupName = this.route.snapshot.paramMap.get('groupName');
  groupMembers = [];

  constructor(private route: ActivatedRoute, private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any>('/getGroupMembers?groupName=' + this.groupName)
      .subscribe(data => {
        console.log(data);
        this.groupMembers = data.memberlist;
      });
  }

  startAR() {
    location.href = '/webXR?groupname=' + this.groupName;
  }
}
