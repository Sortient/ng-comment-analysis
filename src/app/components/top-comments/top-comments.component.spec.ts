import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopCommentsComponent } from './top-comments.component';

describe('TopCommentsComponent', () => {
  let component: TopCommentsComponent;
  let fixture: ComponentFixture<TopCommentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopCommentsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopCommentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
