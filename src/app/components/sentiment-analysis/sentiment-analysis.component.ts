import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-sentiment-analysis',
  templateUrl: './sentiment-analysis.component.html',
  styleUrls: ['./sentiment-analysis.component.css'],
})
export class SentimentAnalysisComponent implements OnInit {
  totalComments = 1245; // Example data
  positivePercentage = 75;
  negativePercentage = 25;

  recentComments = [
    {
      text: 'Great work on the recent changes!',
      sentiment: 'Positive',
      author: 'John Doe',
      date: '2025-01-23',
    },
    {
      text: 'I think this implementation can be optimized.',
      sentiment: 'Neutral',
      author: 'Jane Smith',
      date: '2025-01-22',
    },
    {
      text: 'This approach introduces several issues.',
      sentiment: 'Negative',
      author: 'DevUser123',
      date: '2025-01-21',
    },
  ];

  constructor() {}

  ngOnInit(): void {
    // Initialize or fetch data here
  }
}
