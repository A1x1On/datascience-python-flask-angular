import { Component              } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from  '@angular/forms';
import { DomSanitizer           } from '@angular/platform-browser';
import { Subscription           } from 'rxjs';


import { AccountService         } from '../services/account.service';
import { ToasterService         } from 'angular2-toaster';
import { AppGlobal              } from '../app.global';

import * as $ from 'jquery'

export interface Pattern {
  value : string;
  text  : string;
}

@Component({
  selector: 'app-home',
  templateUrl : './home.component.html'
})

export class HomeComponent {
  public message = `Angular Universal`;
  public image   = 'https://camo.githubusercontent.com/81f72f2fdf98aa1d30b5b215bc8ca9420b249e81/68747470733a2f2f616e67756c61722e696f2f67656e6572617465642f696d616765732f6d61726b6574696e672f636f6e636570742d69636f6e732f756e6976657273616c2e706e67';

  trained       : any;
  files         : any;
  classifier    : number;
  score         : any;
  pattern       : string;
  busy          : Subscription;
  patternValues : Pattern[] = [
    {value: 'risk-company', text: 'Risks of Company'},
    {value: 'titanic'     , text: 'Titanic (example)'},
    {value: 'custom'      , text: 'Custom'}
  ];
  constructor(private accountService : AccountService,
              private app            : AppGlobal,
              private sanitizer      : DomSanitizer,
              private toasterService : ToasterService) {
    this.trained    = '';
    this.classifier = 1;
    this.score      = null;
    this.pattern    = 'titanic';
    this.files      = {
      train : null,
      test  : null
    };
  }

  ngOnInit() {
    $('.html-trained').fadeOut(1);
    // this.annn       = this.accountService.getConfig().subscribe((response) => {
    //   console.log('response ', response);
    // }, (e) => {
    //   console.log('e', this.app.reqError(e));
    // });
  }


  submission() {
    const formData = new FormData();
    console.log('test ', this.app.config.toaster);

    if(this.files.train[0] == undefined){
      this.toasterService.pop('info', 'Please, select "train.csv" first/at least');
      return true;
    }

    let train = this.files.train[0];
    formData.append('train', train.file, train.name);

    if(this.files.test[0] != undefined){
      let test  = this.files.test[0];
      formData.append('test', test.file, test.name);
    }

    this.busy = this.accountService.upload(formData).subscribe(
      (res) => {
        res.classifier = this.classifier;
        res.pattern    = this.pattern;

        return this.getSubResults(res);
      },
      (err) => console.log('err ', err)
    );
  }

  getSubResults(criteria){
    this.busy = this.accountService.getSubResults(criteria).subscribe(
      (res) => {
        let result   = JSON.parse(res.match(/\{.*\}/g)[0]);
        this.score   = result.score;
        res          = res.replace(/\{.*\}/g, '');
        this.trained = this.sanitizer.bypassSecurityTrustHtml(res);

        $('.html-trained').fadeIn(1000);
        return true;
      },
      (err) => console.log('err ', err)
    );
  }

  expandGrid(){
    if($('.html-trained').height() == 531){
      $('.html-trained').animate({height: '100%'}, 2000);
    }else{
      $('.html-trained').animate({height: '531px'}, 500);
    }
  }
}
