import {Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-freunde',
  templateUrl: './friends.component.html',
  styleUrls: ['./friends.component.scss']
})
export class FriendsComponent implements OnInit {
  friends = [];
  friendMail: String = "";

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.updateFriends();
  }

  updateFriends() : void{
    this.http.get<any>('/getFriends')
      .subscribe(data => {
        console.log(data.friendlist);
        this.friends = data.friendlist;
      });
  }

  addFriend(friendMail: String): void {
    this.http.post('/addFriend', friendMail)
      .subscribe(
        data => {
          console.log('success', data)
          this.updateFriends();
        },
        error => {
          console.log('error: ', error)
          if(error.status == 409){
            alert("Nutzer existiert bereits in Freundesliste");
          } else if(error.status == 40){
            alert("Kein Nutzer mit dieser Mail vorhanden!");
          }
        }
      );
    this.friendMail = "";
  }

  deleteFriend(name: string) {
    this.http.delete('/deleteFriend/' + name)
      .subscribe(
        data => {
          console.log('success', data)
          this.updateFriends();
        },
        error => {
          console.log('error: ', error)
        }
      );
  }
}
