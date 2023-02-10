import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GroupsComponent } from './groups/groups.component';

import { FormsModule } from '@angular/forms';
import { GroupDetailComponent } from './group-detail/group-detail.component';
import { CreateGroupComponent } from './create-group/create-group.component';
import { FriendsComponent } from './friends/friends.component';
import { LoginComponent } from './login/login.component'; // <-- NgModel lives here

@NgModule({
  declarations: [
    AppComponent,
    GroupsComponent,
    GroupDetailComponent,
    CreateGroupComponent,
    FriendsComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
