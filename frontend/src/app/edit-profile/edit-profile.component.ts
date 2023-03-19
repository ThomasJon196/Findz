import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from "@angular/router";


@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {
  images = [{id: "", source: "", checked: false}];

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit(): void {
    this.images = [{
      id: "0",
      source: "/static/Tobias.JPG",
      checked: false
    }, {
      id: "1",
      source: "/static/Thomas.JPG",
      checked: false
    }, {
      id: "2",
      source: "/static/Wiete.JPG",
      checked: false
    }, {
      id: "3",
      source: "/static/Ida.JPG",
      checked: false
    }, {
      id: "4",
      source: "/static/Ivy.JPG",
      checked: false
    }
    ];
  }

  save() {
    let chosenImageSource = this.images.filter(x => x.checked).map(y => y.source)[0];
    if (chosenImageSource == undefined) {
      alert("Bitte Bild auswählen!");
      return;
    }

    this.http.post<any>('/updateImage', JSON.stringify({chosenImageSource: chosenImageSource}))
      .subscribe(data => {
        console.log(data);
        this.router.navigate(['gruppen']);
      });
  }
}
