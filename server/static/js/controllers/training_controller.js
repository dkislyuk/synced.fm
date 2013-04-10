function TrainingController($scope, $routeParams, TrainingSet) {
  var training_set = TrainingSet.get($routeParams.train_id).data;

  console.log("this is right after get");
}

function TrainingFormsController($scope, $location, TrainingSet) {
  var trainingSet = new TrainingSet();

  $scope.files = [];
  $scope.name = "";
  $scope.config = {
    'mfcc_step_size': 256,
    'mfcc_block_size': 512,
    'num_components': 6,
    'em_epsilon': 0.01,
    'em_iter': 100
  };

  $scope.pickFiles = function() {

    $scope.files = [{"url":"https://www.filepicker.io/api/file/5wh3Ix5UTgWqvQXCv8bi","filename":"turntable  Trance Out!.html","mimetype":"text/html","size":5243,"isWriteable":true}];
    $scope.selected = true;
    // filepicker.pickMultiple(function(fpfiles) {
    //   $scope.files = fpfiles;

    //   // _.each(fpfiles, function(file) {

    //   // });

    //    console.log(JSON.stringify(fpfiles));


    // });
  };

  $scope.save = function() {
    trainingSet.s3_links = $scope.files;
    trainingSet.name = $scope.name;
    trainingSet.config = $scope.config;

    trainingSet.create().then(function(resp) {
      console.log(resp);
      $location.path("/training/" + resp.id);
    });
  };
}
