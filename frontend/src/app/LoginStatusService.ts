import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoginStatusService {
  isLoggedIn = true;

  setLoginStatus(status: boolean) {
    this.isLoggedIn = status;
  }
}
