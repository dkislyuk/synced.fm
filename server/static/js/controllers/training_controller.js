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
    'em_iter': 100,
    'audio_freq': 16000,
    'cv_type': 'diag',
    'sample_step_size': 1,
    'sample_length': 5
  };

  $scope.pickFiles = function() {
    $scope.files = [{"url":"https://www.filepicker.io/api/file/gR15U71kR1CJws5sh5VC","filename":"cherry_16000.mp3","mimetype":"audio/mpeg","size":1793822,"isWriteable":true}];
    $scope.selected = true;


    // filepicker.pickMultiple(function(fpfiles) {
    //   $scope.files = fpfiles;
    //   $scope.selected = true;
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
