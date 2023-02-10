import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CreateGroupComponent} from './create-group/create-group.component';
import {FriendsComponent} from './friends/friends.component';
import {GroupDetailComponent} from './group-detail/group-detail.component';

import {GroupsComponent} from './groups/groups.component';
import {LoginComponent} from './login/login.component';

const routes: Routes = [
  {path: '', redirectTo: '/login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'gruppen', component: GroupsComponent},
  {path: 'gruppeErstellen', component: CreateGroupComponent},
  {path: 'gruppenDetails/:id', component: GroupDetailComponent},
  {path: 'freunde', component: FriendsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
