import { Component              } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from  '@angular/forms';
import { DomSanitizer           } from '@angular/platform-browser';


import { AccountService         } from '../services/account.service';
import { ToasterService         } from 'angular2-toaster';
import { AppGlobal              } from '../app.global';

import * as $ from 'jquery'

@Component({
  selector: 'app-home',
  templateUrl : './home.component.html'
})
export class HomeComponent {
  public message = `Angular Universal`;
  public image   = 'https://camo.githubusercontent.com/81f72f2fdf98aa1d30b5b215bc8ca9420b249e81/68747470733a2f2f616e67756c61722e696f2f67656e6572617465642f696d616765732f6d61726b6574696e672f636f6e636570742d69636f6e732f756e6976657273616c2e706e67';

  annn      : any;
  str1      : string;
  resavg    : any;
  imgSB    : any;
  imgsrc2   : any;
  imgMiss   : any;
  _sanitizer : DomSanitizer;
  pandas    : any;
  trained   : any;

  empty    : boolean;

  files     : any;
  classifier : number;
  gender : any;
  score: any;

  constructor(private accountService : AccountService,
              private app            : AppGlobal,
              private sanitizer      : DomSanitizer,
              private toasterService : ToasterService,
              private formBuilder    : FormBuilder) {

    this.pandas = '';
    this.trained = '';
    this.classifier = 1;
    this.score      = null;



    this.files = {
      train : null,
      test  : null
    };


  }

  ngOnInit() {
    console.log('-------------ngOnInit------------------');

    $('.html-trained').fadeOut(1);

    this.annn       = this.accountService.getConfig().subscribe((response) => {
      console.log('response ', response);
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
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

    console.log('this.files ', this.files);
    this.accountService.upload(formData).subscribe(
      (res) => {
        console.log('res11111 ', res);

        res.classifier = this.classifier;

        // если один то вернуть колонки с грида для ручного заполнения
        return this.getSubResults(res);
      },
      (err) => console.log('err ', err)
    );
  }


  getSubResults(criteria){
    this.accountService.getSubResults(criteria).subscribe(
      (res) => {

        let result = JSON.parse(res.match(/\{.*\}/g)[0]);

        this.score = result.score;

        console.log('json ', result);

        res = res.replace(/\{.*\}/g, '');

        console.log('res ', res);

        this.trained = this.sanitizer.bypassSecurityTrustHtml(res);

        $('.html-trained').fadeIn(1000);

        return true;
      },
      (err) => console.log('err ', err)
    );
  }

  expandGrid(){


    console.log('$(\'.html-trained\').height() ', $('.html-trained').height());
    if($('.html-trained').height() == 531){
      $('.html-trained').animate({height: '100%'}, 2000);
    }else{
      $('.html-trained').animate({height: '531px'}, 500);
    }



  }



























  getAvg(){
    this.accountService.getAvg({val: this.str1}).subscribe((response) => {
      this.resavg = response;
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }

  getImage(){
    this.accountService.getImage().subscribe((response) => {
      console.log('response ', response);
      this.imgsrc2 = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(response));
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }

  getData(){
    this.accountService.getData().subscribe((response) => {
      console.log('response ', response);
      this.pandas = this.sanitizer.bypassSecurityTrustHtml(response);
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }

  getMissingData(){
    this.accountService.getMissingData().subscribe((response) => {
      console.log('response ', response);
      this.imgSB = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(response));
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }

  getSBData(){
    this.accountService.getSBData().subscribe((response) => {
      console.log('response ', response);
      this.imgSB = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(response));
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }

  getTrained(){
    this.accountService.getTrained().subscribe((response) => {
      console.log('response ', response);
      this.trained = this.sanitizer.bypassSecurityTrustHtml(response);
    }, (e) => {
      console.log('e', this.app.reqError(e));
    });
  }



}
