import { Injectable, OnInit    } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import * as moment               from 'moment';
import * as _                    from 'underscore';

import { ToasterConfig         } from 'angular2-toaster';

@Injectable()
export class AppGlobal {
  static CONFIG = {};

  config: any     = {
    ...AppGlobal.CONFIG,

    toaster: new ToasterConfig({
      showCloseButton   : false,
      tapToDismiss      : true,
      timeout           : 5000,
      animation         : 'fade',
      positionClass     : 'toast-bottom-right',
      mouseoverTimerStop: true
    })
  };

  tempPass : any;
  badge    : any;
  //session  : Account = null;
  remember : any     = {
    checked     : false,
    login_email : null
  };

  constructor() {
    this.rememberMe();
  }

  rememberMe(){
    let remember = localStorage.getItem('remember');
    if(remember)
      this.remember = JSON.parse(remember);
  }

  reqError(e) {
    return e.error != null && e.error.message != undefined ? e.error.message : 'Sorry, something went wrong: ' + e.statusText;
  }

  getDateTypes() {
    return [
      {text : 'This Month'    , value: 1 },
      {text : 'Today'         , value: 2 },
      {text : 'Yesterday'     , value: 3 },
      {text : 'Custom'        , value: 0 },
      {text : 'Last 24 Hours' , value: 4 },
      {text : 'Last 48 Hours' , value: 5 },
      {text : 'Last 72 Hours' , value: 6 },
      {text : 'Last 7 Days'   , value: 7 },
    ];
  }

  getDateByType(period, flag) {
    let date: any;

    switch (period + flag) {
      // This Month
      case '1from' : { date = moment().startOf('month');                                     break; }
      case '1to'   : { date = moment().endOf  ('month');                                     break; }

      // Today
      case '2from' : { date = moment().startOf('day');                                       break; }
      case '2to'   : { date = moment().endOf('day');                                         break; }

      // Yesterday
      case '3from' : { date = moment().startOf('day').subtract(1, 'day');                    break; }
      case '3to'   : { date = moment().endOf('day').subtract(1, 'day');                      break; }

      // Last 24 Hours
      case '4from' : { date = moment().subtract(24, 'hour');                                 break; }

      // Last 48 Hours
      case '5from' : { date = moment().subtract(48, 'hour');                                 break; }

      // Last 72 Hours
      case '6from' : { date = moment().subtract(72, 'hour');                                 break; }

      // Last 7 Days
      case '7from' : { date = moment().subtract(7 , 'day') ;                                 break; }

      default      : { date = moment();                                                      break; }
    }

    return date;
  }
}
