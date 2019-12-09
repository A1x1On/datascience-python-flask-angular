import { Component, Inject              } from '@angular/core';
import { FormBuilder, FormGroup, FormControl } from  '@angular/forms';
import { DomSanitizer           } from '@angular/platform-browser';
import { HttpClient             } from '@angular/common/http';
import { Subscription           } from 'rxjs';
import * as _                     from 'underscore';


import { AccountService         } from '../services/account.service';
import { ToasterService         } from 'angular2-toaster';
import { AppGlobal              } from '../app.global';

import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

import * as $ from 'jquery'

export interface Select {
  value : string;
  text  : string;
}

export interface DialogData {
  animal: string;
  name: string;
}

export interface PeriodicElement {
  name            : string;
  position        : number;
  accuracy_score  : number;
  f1_score        : number;
  recall_score    : number;
  precision_score : number;
}

@Component({
  selector: 'score-dialog',
  templateUrl: './score.dialog.html',
})
export class DialogScore {
  scoreValues: PeriodicElement[] = [
    {position: 1, name: 'LogisticRegression'        , accuracy_score: 0.903, f1_score: 0.893, recall_score: 0.903, precision_score: 0.910},
    {position: 2, name: 'KNeighborsClassifier'      , accuracy_score: 0.897, f1_score: 0.894, recall_score: 0.897, precision_score: 0.902},
    {position: 3, name: 'DecisionTreeClassifier'    , accuracy_score: 0.862, f1_score: 0.835, recall_score: 0.862, precision_score: 0.827},
    {position: 4, name: 'RandomForestClassifier'    , accuracy_score: 0.882, f1_score: 0.870, recall_score: 0.882, precision_score: 0.878},
    {position: 5, name: 'CombinedModels'            , accuracy_score: 0.918, f1_score: 0.907, recall_score: 0.918, precision_score: 0.910}
  ];

  displayedColumns: string[] = ['position', 'name', 'accuracy_score', 'f1_score', 'recall_score', 'precision_score'];

  constructor(
    public dialogRef: MatDialogRef<DialogScore>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

}


@Component({
  selector    : 'app-home',
  templateUrl : './home.component.html'
})

export class HomeComponent {
  public message = `Angular Universal`;
  public image   = 'https://camo.githubusercontent.com/81f72f2fdf98aa1d30b5b215bc8ca9420b249e81/68747470733a2f2f616e67756c61722e696f2f67656e6572617465642f696d616765732f6d61726b6574696e672f636f6e636570742d69636f6e732f756e6976657273616c2e706e67';

  animal: string;
  name: string;



  trained       : any;
  files         : any;
  trainFile     : any;
  classifier    : number;
  score         : any;
  isEdit        : boolean;
  isManual      : boolean;
  isRaw         : boolean;
  manualExpend  : boolean;
  manualTest    : string;
  pattern       : string;
  testEditing   : boolean;
  test          : any;
  tests         : any;
  busy          : Subscription;
  riskValues    : Select[] = [
    {value: 'credit', text: 'Credit'},
    {value: 'denial', text: 'Denial'}
  ];
  patternValues : Select[] = [
    //{value: 'titanic'     , text: 'Titanic (example)'},
    //{value: 'custom'      , text: 'Custom'}
    {value: 'risk-company', text: 'Risks of Company'}
  ];

  constructor(private accountService : AccountService,
              private app            : AppGlobal,
              private http           : HttpClient,
              public  dialog         : MatDialog,
              private sanitizer      : DomSanitizer,
              private toasterService : ToasterService) {
    this.trained      = '';
    this.classifier   = 1;
    this.isEdit       = false;
    this.isManual     = true;
    this.isRaw        = false;
    this.manualExpend = false;
    this.manualTest   = '';
    this.score        = null;
    this.trainFile    = null;
    this.pattern      = 'risk-company';
    this.testEditing  = false;
    this.reset();
    this.tests        = [];
    this.files        = {
      train : null,
      test  : null
    };
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogScore, {
      width: '1250px',
      data: {name: this.name, animal: this.animal}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  reset(){
    this.test = {
      r3   : null,
      r4   : null,
      r5   : null,
      l1   : null,
      l2   : null,
      p1   : null,
      a2   : null,
      a4   : null,
      a1a5 : null,
      a6   : null,
      f1   : null,
      f2   : null,
      f3   : null,
      f4   : null,
      r6   : null,
      l3   : null,
      a1a1 : null,
      a1a3 : null,
      f1f8 : null,
      f11  : null,
      p2   : null
    };
  }

  ngOnInit() {
    $('.html-trained').fadeOut(1);





  }

  addTestRow(){
    this.tests.push({...this.test, id: this.tests.length + 1});
  }

  editTestRow(){
    this.tests = _.map(this.tests, t => {
      if(t.id == this.test.id)
        return this.test;
      return t
    });
    this.resetTest();
  }

  remove(test){
    this.tests = _.reject(this.tests, t => t.id == test.id);
  }

  resetTest(){
    this.testEditing = false;
    this.reset();
    $('.asTable__table tbody tr').removeClass('colorActive1');
  }

  selectTest(t, e){
    $('.asTable__table tbody tr').removeClass('colorActive1');

    $(e.path[1]).addClass('colorActive1');
    this.test        = { ...t };
    this.testEditing = true;
  }

  fillManually(){
    this.isEdit = !this.isEdit;

    setTimeout(function() {
      $('.switcher_manual').addClass('pink-background');
      $('.switcher_raw')   .removeClass('pink-background');
    } , 1);

    if(!this.isEdit)
      this.manualTest = '';
  }

  switcher(flag){
    this.isManual = false;
    this.isRaw    = false;
    $('.switcher_manual').removeClass('pink-background');
    $('.switcher_raw')   .removeClass('pink-background');

    if(flag == 1){
      $('.switcher_manual').addClass('pink-background');
      this.isManual = true;
    }else if(flag == 2){
      $('.switcher_raw').addClass('pink-background');
      this.isRaw = true;
    }

    setTimeout(() => {
      if(this.manualExpend)
        $('.asTable').addClass('w-1800');
    } , 1);
  }

  expandManual(){
    this.manualExpend = !this.manualExpend;
    if(this.manualExpend){
      $('section')             .addClass('max-w-100perI');
      $('.edit-field textarea').addClass('fs-135');
      $('.edit-field')         .addClass('w-97perI');
      $('.edit-field')         .addClass('p-0I');
      $('.asTable')            .addClass('w-1800');
      $('.asTable__table')     .addClass('fonSize9');
      $('.btnTip')             .addClass('left-36');
    }else{
      $('section')             .removeClass('max-w-100perI');
      $('.edit-field textarea').removeClass('fs-135');
      $('.edit-field')         .removeClass('w-97perI');
      $('.edit-field')         .removeClass('p-0I');
      $('.asTable')            .removeClass('w-1800');
      $('.asTable__table')     .removeClass('fonSize9');
      $('.btnTip')             .removeClass('left-36');
    }
  }

  submission() {
    let formData = new FormData();
    let testCSV  = '';

    if(this.isEdit && this.isManual){
      if(!this.tests.length)
        return this.toasterService.pop('error', 'No one test has not been found');

      testCSV              = 'R3;R4;R5;L1;L2;P1;A2;A4;1/A5;A6;F1;F2;F3;F4;R6;L3;1/A1;1/A3;1/F8;F11;P2;binaryrisk\n';
      _.each(this.tests, t => {
         testCSV = testCSV + (!t.r3   ? '0;' : t.r3  .toString() + ';') +
                             (!t.r4   ? '0;' : t.r4  .toString() + ';') +
                             (!t.r5   ? '0;' : t.r5  .toString() + ';') +
                             (!t.l1   ? '0;' : t.l1  .toString() + ';') +
                             (!t.l2   ? '0;' : t.l2  .toString() + ';') +
                             (!t.p1   ? '0;' : t.p1  .toString() + ';') +
                             (!t.a2   ? '0;' : t.a2  .toString() + ';') +
                             (!t.a4   ? '0;' : t.a4  .toString() + ';') +
                             (!t.a1a5 ? '0;' : t.a1a5.toString() + ';') +
                             (!t.a6   ? '0;' : t.a6  .toString() + ';') +
                             (!t.f1   ? '0;' : t.f1  .toString() + ';') +
                             (!t.f2   ? '0;' : t.f2  .toString() + ';') +
                             (!t.f3   ? '0;' : t.f3  .toString() + ';') +
                             (!t.f4   ? '0;' : t.f4  .toString() + ';') +
                             (!t.r6   ? '0;' : t.r6  .toString() + ';') +
                             (!t.l3   ? '0;' : t.l3  .toString() + ';') +
                             (!t.a1a1 ? '0;' : t.a1a1.toString() + ';') +
                             (!t.a1a3 ? '0;' : t.a1a3.toString() + ';') +
                             (!t.f1f8 ? '0;' : t.f1f8.toString() + ';') +
                             (!t.f11  ? '0;' : t.f11 .toString() + ';') +
                             (!t.p2   ? '0;' : t.p2  .toString() + ';') + t.risk + '\n';
      });
    }else if(this.isEdit && this.isRaw){
      if(!this.manualTest)
        return this.toasterService.pop('error', 'Test raw field is empty');

      let i    = 20;
      testCSV  = 'R3;R4;R5;L1;L2;P1;A2;A4;1/A5;A6;F1;F2;F3;F4;R6;L3;1/A1;1/A3;1/F8;F11;P2;binaryrisk\n';
      this.manualTest.trim().replace(/\t/g, ';').split(/\n|;| /g).forEach((val, key) => {
        if(i == key){
          testCSV = testCSV + val + ';';
          testCSV = testCSV + 'binarynullval' + '\r';
          i       = i + 21;
        }else{
          testCSV = testCSV + val + ';';
        }
      });

      // 0,140197592;-0,0226437364;-0,508101417;0,228602326;0,183020413;0,481158687;1,50411276;4,30358762;0,207788298;2,13172161;-1,47191079;0,446974239;-1,12626183;0,0809678455;2,98762455;0,484131209;0,0172192235;0,617430453;0,0643489114;0,27437091;0,386199238
      // 0,213436197;-0,0243794166;-0,650289773;0,269583625;0,140657494;0;1,55079001;5,38566955;0,778022815;3,5004487;-1,97107788;0,527104441;-0,146319004;0,0540889814;2,42833972;0,348174582;0,0255711755;0,467825705;0,163773826;0,003627157;0,385536095
      // 0,1111753;-0,0372754165;-0,20092562;0,584013439;0,161838224;0;0,876979346;4,29972759;0,237475394;2,90707057;2,80146323;0,423083745;-1,33477781;0,0743883572;1,67920374;0,477485714;0,0196915726;0,518398768;0,022191915;0,0675880839;0,131637322
      // 0,0714368655;-0,0174959258;-1,05842664;0,195766945;0,179644157;0,0734283224;1,23844541;5,90047792;0,140307027;3,40319312;2,87639671;0,660487604;-0,289707268;0,0240661781;1,62022728;0,335765591;0,0184169756;0,483942503;0,115443348;0,177347304;0,272153792
      // 0,806161351;0,148945087;0,321058742;0,969247557;0,254500369;2,27369609;1,97468327;2,65686636;0;3,11178584;1,35541848;0,512085242;1,77157926;0,152011531;1,49048962;0,664724117;0;0,302104278;0,613016112;0,967213727;0,636554931
    }

    if(testCSV){
      testCSV = testCSV.slice(0,-1);
      formData.append('test', new Blob([testCSV], {type: "text/plain"}), 'manual-test.csv');
    } else if(this.files.test[0] != undefined){
      let test  = this.files.test[0];
      formData.append('test', test.file, test.name);
    }else{
      return this.toasterService.pop('error', 'Test data is absence');
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
