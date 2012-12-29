/* Auth module, with a controller for the site-wide modal-window login and a service to
		to check user status at the initial app load */
var auth = angular.module('synced.auth', []);

auth.controller({
  LoginController: function($scope, $rootScope, $http, authService) {
  	var user = {
    	username : '',
    	password : ''
    }

  	$scope.form = angular.copy(user);

    $scope.submit = function() {
    	$http.post('/api/user/login', $scope.form).
    		success(function(data) {
          console.log(data);
	   	  	$rootScope.user = data;
	   	  	authService.loginConfirmed();
   			}).
   			error(function(data) {
   				$scope.error = data;
   			});
    };

    $scope.$on('event:auth-loginConfirmed', function(e) {
      $('#login-modal').trigger('reveal:close');
      $scope.name = $rootScope.user.username;

			$scope.status = 'active';
		});

		$scope.$on('event:auth-loginRequired', function(e) {
			/* Activate modal */
		});

		$scope.$on('event:auth-logout', function(e) {
			$scope.status = 'login';
			$scope.name = '';
		});

		$scope.status = 'login';
    $scope.name = 'blank'
  }
});

/* User Status Controller */
auth.service('userService', function($rootScope, $http, authService) {
	/* Logs in the user on initial app load */
	this.status = function() {

  }

  /* Logs out user */
  this.logout = function() {
  	$rootScope.$broadcast('event:auth-logout');
  };
});


/**
 * @license HTTP Auth Interceptor Module for AngularJS
 * (c) Witold Szczerba
 * License: MIT
 */
auth.provider('authService', function() {
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
      	console.log("confirming login");
        $rootScope.$broadcast('event:auth-loginConfirmed');
        retryAll();
      }
    }
  }]
});

/**
 * $http interceptor.
 * On 401 response - it stores the request and broadcasts 'event:angular-auth-loginRequired'.
 */
auth.config(['$httpProvider', 'authServiceProvider', function($httpProvider, authServiceProvider) {
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
}]);
