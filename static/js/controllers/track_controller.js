function TrackController($scope, $http, $routeParams, Track) {
  var track = Track.get({track_id : $routeParams.track_id})
}


function TrackFormsController($scope, Track) {
  var track = {
    title : '',
    artist_info : [{
      artists : [{
        name: '',
        type: 'primary'
      }],
      artist_format : '',
      from_track: 0,
      hidden: []
    }],
    base_track: [],
    track_id: 0,
    modifier: {},
    derivatives: [],
    mixes: [],
    tags: []
  };
 
  $scope.cancel = function() {
    $scope.form = angular.copy(track);
  };
 
  $scope.save = function() {
    var params = $scope.form;
    console.log("saving...", params)

    Track.save(params, function(data) {
      console.log("success: ", data);
    });

  };
 
  $scope.addContact = function() {
    $scope.form.contacts.push({type:'', value:''});
  };
 
  $scope.removeContact = function(contact) {
    var contacts = $scope.form.contacts;
    for (var i = 0, ii = contacts.length; i < ii; i++) {
      if (contact === contacts[i]) {
        contacts.splice(i, 1);
      }
    }
  };
 
  $scope.isCancelDisabled = function() {
    return angular.equals(track, $scope.form);
  };
 
  $scope.isSaveDisabled = function() {
    return false; //return $scope.track_form.$invalid || angular.equals(track, $scope.form);
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
  }
  $scope.cancel();
}