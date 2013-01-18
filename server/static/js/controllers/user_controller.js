function UserSignupController($scope, User, userService) {
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
      userService.signupComplete(data);
    });
  };
}
