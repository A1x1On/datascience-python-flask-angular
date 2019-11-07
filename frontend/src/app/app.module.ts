import { BrowserModule                        } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule     } from '@angular/forms';
import { NgModule                             } from '@angular/core';
import { RouterModule                         } from '@angular/router';
import { BrowserAnimationsModule              } from '@angular/platform-browser/animations';
import { MatIconModule, MatCardModule,
         MatButtonModule, MatFormFieldModule,
         MatRadioModule, MatSelectModule      } from '@angular/material';
import { InputFileConfig, InputFileModule     } from 'ngx-input-file';
import { ToasterModule                        } from 'angular2-toaster';
import { NgBusyModule                         } from 'ng-busy';

import { AppComponent                         } from './app.component';
import { HomeComponent                        } from './home/home.component';
import { HttpClientModule                     } from '@angular/common/http';
import { AccountService                       } from './services/account.service';

import { HttpErrorHandlerService              } from './common/http-error-handler.service';
import { AppGlobal                            } from './app.global';


const config: InputFileConfig = {};

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule.withServerTransition({appId: 'my-app'}),
    FormsModule,
    ReactiveFormsModule,
    ToasterModule.forRoot(),
    RouterModule .forRoot([
      {path: '', component: HomeComponent, pathMatch: 'full'},
      {path: 'lazy', loadChildren: './lazy/lazy.module#LazyModule'},
      {path: 'lazy/nested', loadChildren: './lazy/lazy.module#LazyModule'}
    ]),
    HttpClientModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatButtonModule,
    MatFormFieldModule,
    MatRadioModule,
    MatSelectModule,
    MatIconModule,
    NgBusyModule,
    InputFileModule.forRoot(config)
  ],
  providers: [AccountService, HttpErrorHandlerService, AppGlobal],
  bootstrap: [AppComponent]
})
export class AppModule { }
