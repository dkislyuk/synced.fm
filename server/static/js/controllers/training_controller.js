function TrainingController($scope, $routeParams, TrainingSet) {
  var training_set = TrainingSet.get($routeParams.train_id);
}

function TrainingFormsController($scope, $location, TrainingSet) {
  var trainingSet = new TrainingSet();

  $scope.files = [];
  $scope.name = "";

  $scope.pickFiles = function() {

    $scope.files = [{"url":"https://www.filepicker.io/api/file/5wh3Ix5UTgWqvQXCv8bi","filename":"turntable  Trance Out!.html","mimetype":"text/html","size":5243,"isWriteable":true}];

    // filepicker.pickMultiple(function(fpfiles) {
    //   $scope.files = fpfiles;

    //   // _.each(fpfiles, function(file) {

    //   // });

    //    console.log(JSON.stringify(fpfiles));


    // });
  };

  $scope.submit = function() {
    trainingSet.files = $scope.files;
    trainingSet.name = $scope.name;

    trainingSet.create().then(function(resp) {
      console.log(resp);
      $location.path("/training/" + resp.id);


    });
  };
}
