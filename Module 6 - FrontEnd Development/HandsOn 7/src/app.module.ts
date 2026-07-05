import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { CourseListComponent } from './components/course-list/course-list.component';
import { CourseCardComponent } from './components/course-card/course-card.component';
import { StudentProfileComponent } from './components/student-profile/student-profile.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    CourseListComponent,
    CourseCardComponent,
    StudentProfileComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,          // needed this for ngModel, forgot at first and got an error
    ReactiveFormsModule,  // needed for the profile form
    HttpClientModule      // needed for the service to call the api
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
