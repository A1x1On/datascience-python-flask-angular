import {Component} from '@angular/core';
import { AppGlobal          } from './app.global';

@Component({
  selector: 'app-root',
  template: `
    
    <div class="container-wrapper">
      <toaster-container [toasterconfig]="app.config.toaster"></toaster-container>
      <header>

      </header>
      <section>
          <router-outlet></router-outlet>
      </section>
      <footer>

      </footer>
    </div>
   
  `
})
export class AppComponent {
  constructor(
    public  app            : AppGlobal
  ) {
  }
}
