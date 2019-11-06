import { Injectable         } from '@angular/core';
import { HttpErrorResponse  } from '@angular/common/http';
import { Observable, throwError, of     } from 'rxjs';


@Injectable()
export class HttpErrorHandlerService {
  constructor() {
  }

  handleError<T> (error: HttpErrorResponse, operation?: string, result = {} as T) {
    error['operation'] = operation;
    error['entity']    = result;
    return throwError('error');
  }
}




