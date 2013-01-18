function TrackController($scope, $routeParams, Track) {
  var track = Track.get({track_id : $routeParams.track_id});
}


function TrackFormsController($scope, Track, Track2) {
  //var track = Track.get({id: '0'});
  Track2.get(1);

  //console.log(track);
  // var track = {
  //   title : '',
  //   artist_info : [{
  //     artists : [{
  //       name: '',
  //       type: 'primary'
  //     }],
  //     artist_format : '',
  //     from_track: 0,
  //     hidden: []
  //   }],
  //   base_track: [],
  //   track_id: 0,
  //   modifier: {},
  //   derivatives: [],
  //   mixes: [],
  //   tags: []
  // };

  $scope.cancel = function() {
    $scope.form = angular.copy(track);
  };

  $scope.save = function() {
    var params = $scope.form;


    console.log("saving with: ", params);
    Track.save(params, function(data) {
      console.log(data);
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
