import {Component, OnInit} from '@angular/core';
import {LoginStatusService} from '../LoginStatusService';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(public loginStatusService: LoginStatusService) {
    this.loginStatusService.setLoginStatus(false);
  }

  ngOnInit() {
  }
}
