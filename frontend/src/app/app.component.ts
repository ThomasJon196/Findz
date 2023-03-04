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

}
