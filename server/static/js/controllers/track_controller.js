function TrackController($scope, $routeParams, Track) {
  var track = Track.get({track_id : $routeParams.track_id});
}


function TrackFormsController($scope, Track) {
  // Track.get(0).then(function(t) {
  //   track = t;
  //   console.log(t);
  //   $scope.form = angular.copy(track);
  // });


  var track = new Track();
  track.title = '';
  track.artist_info = [{
      artists : [{
        name: '',
        type: 'primary'
      }],
      artist_format : '',
      from_track: 0,
      hidden: []
    }];

  $scope.cancel = function() {
    $scope.form = angular.copy(track);
  };

  $scope.save = function() {
    var params = $scope.form;

    console.log("saving with: ", params);
    track.create().then(function(resp) {
      console.log(resp);
    });
  };

  $scope.isCancelDisabled = function() {
    return angular.equals(track, $scope.form);
  };

  $scope.isSaveDisabled = function() {
    return false;
  };

  /* Begin original track methods */

  $scope.add_artist = function() {
    $scope.form.artist_info[0].artists.push({
      name: '',
      type: 'primary'
    });
  };

  /* Remove artist from original track */
  $scope.remove_artist = function(artist) {
    var artists = $scope.form.artist_info[0].artists;
    for (var i = 0; i < artists.length; i++) {
      if (artist === artists[i]) artists.splice(i, 1);
    }
  };

  $scope.cancel();
}
