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
    /*const cookies = document.cookie.split(';');
    let sessionID = "";
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('sessionId=')) {
        sessionID = cookie.substring('sessionId='.length, cookie.length);
      }
    }
    const httpOptions = {
      withCredentials: true
    };

    this.http.get('/getGroups?sessionId=${sessionId}', httpOptions)
      .subscribe(response => {
        console.log(response);
        //this.groups = response;
      });

     */

    const cookies = document.cookie.split(';');
    let sessionId = "";
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith('sessionId=')) {
        sessionId = cookie.substring('sessionId='.length, cookie.length);
      }
    }
    console.log(sessionId);
    console.log(cookies);

    const url = `/getGroups?sessionId=${sessionId}`;

    fetch(url, {
      method: 'GET',
      credentials: 'include'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
        //this.groups = data;
      })
      .catch(error => {
        console.error('There was an error:', error);
      });

  }
}
