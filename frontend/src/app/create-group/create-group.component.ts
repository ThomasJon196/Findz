import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-create-group',
  templateUrl: './create-group.component.html',
  styleUrls: ['./create-group.component.scss']
})
export class CreateGroupComponent implements OnInit {

  friends = [{name: "Tobi"}, {name: "Thomas"}];
  //friends = [];

  constructor(private http: HttpClient) {
  }

  ngOnInit(): void {
    /*this.http.get('/getFriends')
      .subscribe(response => {
        console.log(response);
        //this.friends = response;
      });

     */
  }

  saveGroup() {

  }
}
