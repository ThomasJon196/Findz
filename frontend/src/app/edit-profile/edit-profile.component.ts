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
      id: "1",
      source: "https://images.unsplash.com/photo-1519750783826-e2420f4d687f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2574&q=80",
      checked: false
    }, {
      id: "2",
      source: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1364&q=80",
      checked: false
    }, {
      id: "3",
      source: "https://images.unsplash.com/photo-1651147538420-06f5e0d3f1d9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MnwxNTc5MTk3fHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60",
      checked: false
    }, {
      id: "4",
      source: "https://images.unsplash.com/photo-1659846490270-58b1e659ddc0?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MXwxNTc5MTk3fHxlbnwwfHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60",
      checked: false
    }];
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
