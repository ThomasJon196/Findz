import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {Group} from '../group';

import {GROUPS} from '../mock-groups';

@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrls: ['./group-detail.component.scss']
})
export class GroupDetailComponent implements OnInit {

  groups = GROUPS;

  currentGroup?: Group;

  constructor(private router: Router) {

    this.currentGroup = this.groups.find((gr) => {
      return gr.id.toString() === this.router.url.substring(16)
    });

  }

  ngOnInit(): void {
  }

}
