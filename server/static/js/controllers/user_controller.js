function UserSignupController($scope, User, userService) {
	//userStatusProvider.set("signing up...");
	//$rootScope.page = "Signup!"

  var user = {
  	email : '',
    username : '',
    password : ''
  };

  $scope.form = angular.copy(user);

  $scope.save = function() {
    var params = $scope.form;
    console.log("creating user...", params)

    User.save(params, function(data) {
      console.log("success: ", data);
    });

    //track = $scope.form;
    //$scope.cancel();
    //var params = $scope.form;

    // $http.post('/api/user/signup', params).success(function(data) {
    //   console.log("user signed up: ", data);
    // });
	//user.set("all done");
	//console.log(userStatusProvider.status);
	   userService.login(params.username);
  };
}

/* MOVE TO http://www.espeo.pl/2012/02/26/authentication-in-angularjs-application */ 
function UserLoginController($scope, User, userService, UserLogin) {
  var user = {
    username : '',
    password : ''
  };

  $scope.form = angular.copy(user);
  
  $scope.login = function() {
    UserLogin.login($scope.form);
  };

}

function UserStatusController($scope) {
	$scope.status = "not logged in"

	$scope.$on('user_login', function(e, data) {
		console.log(e);
		console.log(data);
		$scope.status = data;
	});
	//$scope.user = user.status;
}