import { Component, OnInit  } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  stats: any = {};
  errorMessage: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchStats();
  }

  fetchStats(): void {
    this.apiService.getCommentStats().subscribe({
      next: (data) => {
        this.stats = data;
      },
      error: (error) => {
        console.error('Error fetching stats:', error);
        this.errorMessage = 'Failed to load stats. Please try again later.';
      }
    });
  }
}
