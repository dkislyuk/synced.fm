function TrackController($scope, $routeParams, Track) {
  var track = Track.get({track_id : $routeParams.track_id});
}
