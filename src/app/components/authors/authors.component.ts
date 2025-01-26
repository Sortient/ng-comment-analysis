import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-authors',
  templateUrl: './authors.component.html',
  styleUrls: ['./authors.component.css']
})
export class AuthorsComponent implements OnInit {
  rankedAuthors: any[] = []; // To store authors with comment counts
  errorMessage: string = ''; // Error message (if any)

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchRankedAuthors();
  }

  fetchRankedAuthors(): void {
    this.apiService.getRankedAuthors().subscribe({
      next: (data) => {
        this.rankedAuthors = data; // Populate the list
      },
      error: (error) => {
        console.error('Error fetching ranked authors:', error);
        this.errorMessage = 'Failed to load ranked authors. Please try again later.';
      }
    });
  }
}
