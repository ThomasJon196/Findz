import {Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Person} from "../person";

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
    this.updateFriends();
  }

  updateFriends() : void{
    let response = this.http.get('http://localhost:5000/getFriends')
      .subscribe(response => {
        console.log(response);
      });
    //this.friends = response.
  }

  addFriend(friendMail: String): void {
    let response = this.http.post('http://localhost:5000/addFriend', friendMail)
      .subscribe(response => {
        console.log(response);
      });
    /*if(repsonse.){
      this.updateFriends();
    }else{
      alert("Kein Nutzer mit dieser Mail vorhanden!")
    }
     */
  }

  deleteFriend(name: string) {
    /*let response = this.http.delete('http://localhost:5000/deleteFriend', name)
      .subscribe(response => {
        console.log(response);
      });
     */
    /*if(repsonse.){
      this.updateFriends();
    }else{
      alert("Kein Nutzer mit dieser Mail vorhanden!")
    }
     */
  }
}
