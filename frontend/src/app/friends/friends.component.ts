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
  }

  addFriend(friendMail: String) {
    this.http.post('http://localhost:5000/addFriend', { data: friendMail })
      .subscribe(response => {
        console.log(response);
      });
  }

}
