import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// this service just gets the data from the API
// I put it here so I don't have to write http.get in every component
@Injectable({
  providedIn: 'root'
})
export class CourseService {

  // using jsonplaceholder since we don't have a real backend yet
  apiUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=5';

  constructor(private http: HttpClient) { }

  getCourses(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}
