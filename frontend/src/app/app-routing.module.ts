import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CreateGroupComponent} from './create-group/create-group.component';
import {FriendsComponent} from './friends/friends.component';
import {GroupDetailComponent} from './group-detail/group-detail.component';
import {GroupsComponent} from './groups/groups.component';
import {LoginComponent} from './login/login.component';
import {EditProfileComponent} from "./edit-profile/edit-profile.component";

const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'gruppen', component: GroupsComponent},
  {path: 'gruppeErstellen', component: CreateGroupComponent},
  {path: 'gruppenDetails/:groupName', component: GroupDetailComponent},
  {path: 'freunde', component: FriendsComponent},
  {path: 'profilBearbeiten', component: EditProfileComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
