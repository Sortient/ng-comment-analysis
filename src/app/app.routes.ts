import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ContactComponent } from './components/contact/contact.component';
import { SentimentAnalysisComponent } from './components/sentiment-analysis/sentiment-analysis.component';
import { AuthorsComponent } from './components/authors/authors.component';
import { TopCommentsComponent } from './components/top-comments/top-comments.component';

export const routes: Routes = [
    {
        path: '', redirectTo: 'dashboard', pathMatch: 'full'
    },
    {
        path: 'dashboard', component: DashboardComponent
    },
    {
        path: 'contact', component: ContactComponent
    },
    {
        path: 'sentiment-analysis', component: SentimentAnalysisComponent
    },
    {
        path: 'authors', component: AuthorsComponent
    },
    {
        path: 'top-comments', component: TopCommentsComponent
    }
];
