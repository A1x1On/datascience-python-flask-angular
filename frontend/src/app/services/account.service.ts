import { Injectable                    } from '@angular/core';
import { HttpClient, HttpParams, HttpEventType        } from '@angular/common/http';
import { HttpHeaders                   } from '@angular/common/http';
import { Observable, throwError        } from 'rxjs';
import { catchError, map, tap          } from 'rxjs/operators';

import * as moment                       from 'moment';
import * as _                            from 'underscore';

import { HttpErrorHandlerService       } from '../common/http-error-handler.service';
import { AppGlobal                     } from '../app.global';

@Injectable()
export class AccountService {

  constructor(
    private http           : HttpClient,
    private httpError      : HttpErrorHandlerService,
   // private app            : AppGlobal
  ) {
  }


  public upload(data) {

      console.log('datadatadata ', data);
    return this.http.post<any>('/api/upload', data).pipe(
      catchError(err => {
        return this.httpError.handleError(err, 'getTransactions', {})
      })
    );
  }

  public getSubResults(data) {

    return this.http.post<any>('/api/getSubResults', data, {responseType: 'text' as 'json'}).pipe(
      catchError(err => {
        return this.httpError.handleError(err, 'getTransactions', {})
      })
    );
  }

  getConfig() {


    const header = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Origin': '*',
      'Acffffffffffffffffn': 'sssssssss'
    };


    const httpOptions = new HttpHeaders(header);




    return this.http.get<any>(`/api/board`, {headers : httpOptions})

      .pipe(
          catchError(err => {


            console.log('errerrerrerrerr ', err);
            return this.httpError.handleError(err, 'getTransactions', {})
          })
      )
    ;

  }

  getAvg(criteria) {
    return this.http.get<any>(`/api/getAvg?val=${criteria.val}`)
      .pipe(
        catchError(err => {
          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
    ;

  }

  getImage() {
    return this.http.get<any>(`/api/getImage`,  {responseType: 'blob' as 'json'})
      .pipe(
        catchError(err => {
          console.log('err ', err);

          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
    ;
  }

  getData() {
    return this.http.get<any>(`/api/getData`, {responseType: 'text' as 'json'})
      .pipe(
        catchError(err => {
          console.log('err ', err);
          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
    ;
  }

  getMissingData() {
    return this.http.get<any>(`/api/getMissingData`, {responseType: 'blob' as 'json'})
      .pipe(
        catchError(err => {
          console.log('err ', err);
          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
    ;
  }

  getSBData() {
    return this.http.get<any>(`/api/getSBData`,  {responseType: 'blob' as 'json'})
      .pipe(
        catchError(err => {
          console.log('err ', err);

          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
    ;
  }

  getTrained() {
    return this.http.get<any>(`/api/getTrained`, {responseType: 'text' as 'json'})
      .pipe(
        catchError(err => {
          console.log('err ', err);

          return this.httpError.handleError(err, 'getTransactions', {})
        })
      )
      ;
  }

  _encode(account: Account): void {
    localStorage.setItem('LoggedIn', JSON.stringify(account));
    //this.app.session = account;
  }

  _decode(): Account {
    try {
      return JSON.parse(localStorage.getItem('LoggedIn') || null);
    } catch {
      return null;
    }
  }

}

