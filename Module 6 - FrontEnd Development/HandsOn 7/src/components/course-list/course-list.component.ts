import { Component, OnInit } from '@angular/core';
import { CourseService } from '../../services/course.service';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {

  // storing all courses and the ones we show after search separately
  // probably not the best way but it works
  allCourses: any[] = [];
  coursesToShow: any[] = [];

  searchText = '';
  isLoading = false;

  constructor(private courseService: CourseService) { }

  ngOnInit(): void {
    this.isLoading = true;

    this.courseService.getCourses().subscribe((response) => {
      console.log(response); // just checking what the api gives back

      // jsonplaceholder doesn't actually have course data
      // so I'm just making up fields from the post data for now
      this.allCourses = [];
      for (let i = 0; i < response.length; i++) {
        let post = response[i];
        this.allCourses.push({
          id: post.id,
          name: post.title.substring(0, 20),
          code: 'CS10' + i,
          credits: 3,
          grade: 'A'
        });
      }

      this.coursesToShow = this.allCourses;
      this.isLoading = false;
    }, (error) => {
      console.log('something went wrong', error);
      this.isLoading = false;
    });
  }

  // called every time the user types in the search box
  onSearchChange() {
    if (this.searchText === '') {
      this.coursesToShow = this.allCourses;
      return;
    }

    this.coursesToShow = this.allCourses.filter(course =>
      course.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

}
