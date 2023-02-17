import {Component, OnInit} from '@angular/core';

import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {

  //groups = [];
  groups = [
    {id: 12, name: 'Karneval', members: [{id: 1, name: 'Peter', locationOn: true}]},
    {id: 13, name: 'Geburtstag Tobi', members: [{id: 1, name: 'Peter', locationOn: true}, {id: 3, name: 'Tobias', locationOn: true}]},
    {id: 14, name: 'Feiern', members: [{id: 1, name: 'Peter', locationOn: true}, {id: 2, name: 'Anna', locationOn: false}, {id: 3, name: 'Tobias', locationOn: true}]}
  ];

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    this.updateGroup();
  }

  updateGroup(): void {
    this.http.get('http://localhost:5000/getGroups')
      .subscribe(response => {
        console.log(response);
        //this.groups = response;
      });
  }
}
