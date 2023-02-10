import {Component, OnInit} from '@angular/core';
import {Group} from '../group';

import {GROUPS} from '../mock-groups';

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {

  groups = GROUPS;

  constructor() {
  }

  ngOnInit(): void {
  }

}
