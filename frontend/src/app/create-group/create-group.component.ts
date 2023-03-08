import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";

@Component({
  selector: 'app-create-group',
  templateUrl: './create-group.component.html',
  styleUrls: ['./create-group.component.scss']
})
export class CreateGroupComponent implements OnInit {

  friends = [{name: "", checked: false}];
  groupName: String = "";
  checked = [];

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit(): void {
    this.http.get<any>('/getFriends')
      .subscribe(data => {
        console.log(data);
        this.friends = [];
        data.friendlist.forEach((x: any) => this.friends.push({name: x, checked: false}));
      });
  }

  saveGroup() {
    let members = this.friends.filter(x => x.checked).map(y => y.name);
    if (this.groupName == "") {
      alert("Bitte Gruppennamen eingeben!");
      return;
    } else if (members.length == 0) {
      alert("Bitte Gruppenmitglieder auswählen!");
      return;
    }
    this.http.post<any>('/createGroup', JSON.stringify({members: members, name: this.groupName.trimEnd()}))
      .subscribe(data => {
        console.log(data);
        this.router.navigate(['gruppen']);
      });
  }
}
