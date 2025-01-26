import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-top-comments',
  imports: [CommonModule],
  templateUrl: './top-comments.component.html',
  styleUrl: './top-comments.component.css'
})
export class TopCommentsComponent implements OnInit {
  topPositive: any[] = []; // Top 5 positive comments
  topNegative: any[] = []; // Top 5 negative comments
  errorMessage: string = ''; // Error message (if any)

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchTopComments();
  }

  fetchTopComments(): void {
    this.apiService.getTopComments().subscribe({
      next: (data) => {
        this.topPositive = data.top_positive;
        this.topNegative = data.top_negative;
      },
      error: (error) => {
        console.error('Error fetching top comments:', error);
        this.errorMessage = 'Failed to load top comments. Please try again later.';
      }
    });
  }

  toggleComment(comment: any): void {
    comment.expanded = !comment.expanded; // Toggle the expanded state
  }
}