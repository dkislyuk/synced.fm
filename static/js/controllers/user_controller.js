function UserSignupController($scope, $http, userService) {
	//userStatusProvider.set("signing up...");
	//$rootScope.page = "Signup!"

  var user = {
  	email : '',
    username : '',
    password : ''
  };

  $scope.form = angular.copy(user);

  $scope.save = function() {
    //track = $scope.form;
    //$scope.cancel();
    var params = $scope.form;

    // $http.post('/api/user/signup', params).success(function(data) {
    //   console.log("user signed up: ", data);
    // });
	//user.set("all done");
	//console.log(userStatusProvider.status);
	userService.login(params.username);
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