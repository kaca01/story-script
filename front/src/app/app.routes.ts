import { Routes } from '@angular/router';
import { StoryViewComponent } from './components/pages/story-view/story-view.component';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'story',
        pathMatch: 'full'
    },
    {
        path: 'story',
        component: StoryViewComponent
    }
];
