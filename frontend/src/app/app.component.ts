import { Component } from '@angular/core';
import { LoginStatusService } from './LoginStatusService';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Findz';
  constructor(public loginStatusService: LoginStatusService) {}

  openNav() {
    // @ts-ignore
    document.getElementById("mySidebar").style.width = "140px";
    // @ts-ignore
    document.getElementById("main").style.marginRight = "140px";
  }

  closeNav() {
    // @ts-ignore
    document.getElementById("mySidebar").style.width = "0";
    // @ts-ignore
    document.getElementById("main").style.marginRight= "0";
  }

}
