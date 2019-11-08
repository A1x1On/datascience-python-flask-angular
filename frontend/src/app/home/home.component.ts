import { Component              } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from  '@angular/forms';
import { DomSanitizer           } from '@angular/platform-browser';
import { Subscription           } from 'rxjs';
import * as _                     from 'underscore';


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
  edit          : boolean;
  manualExpend  : boolean;
  manualTest    : string;
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
    this.trained      = '';
    this.classifier   = 1;
    this.edit         = false;
    this.manualExpend = false;
    this.manualTest   = '';
    this.score        = null;
    this.pattern      = 'titanic';
    this.files        = {
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

  fillManually(){
    this.edit = !this.edit;
    if(!this.edit)
      this.manualTest = '';
  }

  expandManual(){
    this.manualExpend = !this.manualExpend;
    if(this.manualExpend){
      $('section')             .addClass('max-w-100perI');
      $('.edit-field textarea').addClass('fs-135');
      $('.edit-field')         .addClass('w-97perI');
      $('.edit-field')         .addClass('p-0I');

    }else{
      $('section')             .removeClass('max-w-100perI');
      $('.edit-field textarea').removeClass('fs-135');
      $('.edit-field')         .removeClass('w-97perI');
      $('.edit-field')         .removeClass('p-0I');
    }
  }

  submission() {
    const formData = new FormData();
    let testCSV    = 'R3;R4;R5;L1;L2;P1;A2;A4;1/A5;A6;F1;F2;F3;F4;R6;L3;1/A1;1/A3;1/F8;F11;P2;binaryrisk\n';

    if(this.manualTest){
      let i       = 21;
      this.manualTest.trim().replace("'", '').split(/\n|;| /g).forEach((val, key) => {
        if(i == key){
          testCSV = testCSV + val + '\r';
          i       = i + 22;
        }else{
          testCSV = testCSV + val + ';';
        }
      });

      testCSV = testCSV.slice(0,-1);
      //-0,508101417;0,228602326;0,183020413;0,481158687;1,50411276;4,30358762;0,207788298;2,13172161;-1,471923379;-1,47191079;0,446974239;-1,12626183;0,0809678455;2,98762455;0,484131209;0,0172192235;0,617430453;0,0643489114;0,27437091;0,386199238;denial
    }


    if(this.files.train[0] == undefined){
      this.toasterService.pop('info', 'Please, select "train.csv" first/at least');
      return true;
    }

    let train = this.files.train[0];
    formData.append('train', train.file, train.name);

    if(this.files.test[0] != undefined){
      let test  = this.files.test[0];
      formData.append('test', test.file, test.name);
    }else if(testCSV){
      formData.append('test', new Blob([testCSV], {type: "text/plain"}), 'test.csv');
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
