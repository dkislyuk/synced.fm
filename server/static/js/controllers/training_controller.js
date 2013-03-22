function TrainingController($scope, $routeParams, TrainingSet) {
  var training_set = TrainingSet.get($routeParams.train_id);
}

function TrainingFormsController($scope, TrainingSet) {
  $scope.pickFiles = function() {
    filepicker.pickMultiple(function(fpfiles){
       console.log(JSON.stringify(fpfiles));
    });
  };
}
