import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CourseListComponent } from './components/course-list/course-list.component';
import { StudentProfileComponent } from './components/student-profile/student-profile.component';

const routes: Routes = [
  { path: '', component: CourseListComponent },
  { path: 'profile', component: StudentProfileComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
