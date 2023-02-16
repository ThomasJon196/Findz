import {Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-freunde',
  templateUrl: './friends.component.html',
  styleUrls: ['./friends.component.scss']
})
export class FriendsComponent implements OnInit {

  friends = [{name: "tobi"}];
  friendMail: String = "";

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    /*this.http.get('http://localhost:5000/getFriends')
      .subscribe(response => {
        console.log(response);
      });

     */
  }

  addFriend(friendMail: String) {
    this.http.post('http://localhost:5000/addFriend', friendMail)
      .subscribe(response => {
        console.log(response);
      });
  }

}
