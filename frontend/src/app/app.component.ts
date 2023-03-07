import {Component} from '@angular/core';
import {LoginStatusService} from './LoginStatusService';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Findz';
  sidebarStyle: any = {"width": "0"};
  mainStyle: any = {"marginRight": "0"};

  constructor(public loginStatusService: LoginStatusService) {
  }

  openNav() {
    this.sidebarStyle = {"width": "140px"};
    this.mainStyle = {"marginRight": "140px"};
  }

  closeNav() {
    this.sidebarStyle = {"width": "0"};
    this.mainStyle = {"marginRight": "0"};
  }
}
