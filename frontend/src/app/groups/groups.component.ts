import {Component, OnInit} from '@angular/core';

import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {

  groups = [];

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    this.updateGroup();
  }

  updateGroup(): void {
    this.http.get<any>('/getGroups')
      .subscribe(data => {
        console.log(data);
        this.groups = data.goruplist;
      });
  }
}
