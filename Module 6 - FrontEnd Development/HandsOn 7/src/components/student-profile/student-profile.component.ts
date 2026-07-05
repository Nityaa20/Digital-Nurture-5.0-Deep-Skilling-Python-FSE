import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.css']
})
export class StudentProfileComponent {

  // building the form here, following what I saw in the angular docs
  profileForm = new FormGroup({
    name: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    semester: new FormControl('', Validators.required)
  });

  onSubmit() {
    // not sending this anywhere yet, just checking it works
    console.log(this.profileForm.value);
    alert('Profile saved (check console)');
  }

}
