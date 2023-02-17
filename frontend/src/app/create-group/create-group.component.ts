import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";

@Component({
  selector: 'app-create-group',
  templateUrl: './create-group.component.html',
  styleUrls: ['./create-group.component.scss']
})
export class CreateGroupComponent implements OnInit {

  friends = [];
  groupName: String = "";
  checked = [];

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit(): void {
    this.http.get<any>('/getFriends')
      .subscribe(data => {
        console.log(data);
        this.friends = data.friendlist
        //this.friends = data.friendlist.forEach((item: any) => {"name": item.toString(), checked: false});
      });
  }

  async saveGroup() {
    console.log(this.groupName);
    await this.http.post<any>('/createGroup', JSON.stringify(this.groupName))
      .subscribe(data => {
        console.log(data);
      });

    //var l = this.friends.filter(f => f.checked==true)

    await this.http.post<any>('/addMembers', JSON.stringify({members: ["test"], name: this.groupName}))
      .subscribe(data => {
        console.log(data);
      });
    await this.router.navigate(['gruppen']);
  }
}
