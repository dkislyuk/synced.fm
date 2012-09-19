var app = angular.module('synced', ['synced.services', 'synced.directives']);
  
app.config(['$routeProvider','$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true),
    $routeProvider.
      /* Track routing */
      when('/track/new',         { templateUrl: '/static/views/track/new.html',   controller: TrackFormsController}).
      when('/track/:track_id',   { templateUrl: '/static/views/track/index.html', controller: TrackController}).

      /* Tag routing */
      //when('/tag/new',           { templateUrl: '/static/views/track/new.html',   controller: TrackFormsController}).
      when('/track/:tag_id',     { templateUrl: '/static/views/track/index.html', controller: TrackController}).

      /* User routing */
      when('/signup',            { templateUrl: '/static/views/user/new.html',    controller: UserSignupController}).
      otherwise({redirectTo: '/track/new'});
}]);

/* User Status Controller */
app.service('userService', function($rootScope) {
  this.login = function(u) {
    $rootScope.$broadcast('user_login', u);    
  };
  this.logout = function() {

  };
});


/* Auth provider: http://www.espeo.pl/2012/02/26/authentication-in-angularjs-application */
app.provider('authService', function() {
  /**
   * Holds all the requests which failed due to 401 response,
   * so they can be re-requested in future, once login is completed.
   */
  var buffer = [];
  
  /**
   * Required by HTTP interceptor.
   * Function is attached to provider to be invisible for regular users of this service.
   */
  this.pushToBuffer = function(config, deferred) {
    buffer.push({
      config: config, 
      deferred: deferred
    });
  }
  
  this.$get = ['$rootScope','$injector', function($rootScope, $injector) {
    var $http; //initialized later because of circular dependency problem
    function retry(config, deferred) {
      $http = $http || $injector.get('$http');
      $http(config).then(function(response) {
        deferred.resolve(response);
      });
    }
    function retryAll() {
      for (var i = 0; i < buffer.length; ++i) {
        retry(buffer[i].config, buffer[i].deferred);
      }
      buffer = [];
    }

    return {
      loginConfirmed: function() {
        $rootScope.$broadcast('event:auth-loginConfirmed');
        retryAll();
      }
    }
  }]
});

app.config(function($httpProvider, authServiceProvider) {
  var interceptor = ['$rootScope', '$q', function($rootScope, $q) {
    function success(response) {
      return response;
    }

    function error(response) {
      if (response.status === 401) {
        var deferred = $q.defer();
        authServiceProvider.pushToBuffer(response.config, deferred);
        $rootScope.$broadcast('event:auth-loginRequired');
        return deferred.promise;
      }
      // otherwise
      return $q.reject(response);
    }

    return function(promise) {
      return promise.then(success, error);
    }

  }];
  $httpProvider.responseInterceptors.push(interceptor);
});

