function TrackController($scope, $http) {
    $http.post('/api/track/123', {}).success(function(data) {
      console.log("finish", data);
    });
}


function TrackFormsController($scope, Track) {
  $scope.templates =
    [ { name: 'Original Track',   url: '<%= asset_path("track/original_track_forms.html") %>'}
    , { name: 'Remix Track',      url: '<%= asset_path("track/remix_track_forms.html") %>'} ];
  $scope.template = $scope.templates[0];

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
    id: '',
    modifier: {},
    derivatives: [],
    mixes: [],

  };
 
  $scope.state = /^\w\w$/;
  $scope.zip = /^\d\d\d\d\d$/;
 
  $scope.cancel = function() {
    $scope.form = angular.copy(track);
  };
 
  $scope.save = function() {
    //track = $scope.form;
    //$scope.cancel();
    var params = $scope.form;
    console.log("saving...")

    // var track_obj = new Track(params);
    // track_obj.$save();

    Track.save(params);

    // $http.post('/api/track/create', params).success(function(data) {
    //   console.log("finish", data);
    // });

    // $http({method: "track", url: "http://0.0.0.0:2727"}).
    //   success(function(data, status) {
    //     console.log("success");
    //     //$scope.status = status;
    //     //$scope.data = data;
    //   }).
    //   error(function(data, status) {
    //     console.log("fail");
    //     //$scope.data = data || "Request failed";
    //     //$scope.status = status;
    // });

    // $http.post('/track/', {}, {
    //   url : 'http://0.0.0.0:2727'
    // }).success(function(data) {
    //   console.log("finish");
    // });
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
    return false;//return $scope.track_form.$invalid || angular.equals(track, $scope.form);
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

  $scope.generate_title = function() {
    // console.log("generating title: ");
    // var result = '';
    // var artist_info = $scope.form.artist_info;
    // console.log("artist info: ", artist_info);
    // for (var i in artist_info) {
    //   var artist_collection = artist_info[i];
    //   //console.log("ac: ", artist_collection);
    //   // for (var j in artist_collection.artists) {
    //   //   result += '& ';
    //   // }
    // }

    // //return result;
    // $scope.generated_title = result;
  }
  
  $scope.cancel();
  $scope.generate_title();
  //$scope.generated_title = $scope.generate_title();
}

function OriginalTrack($scope) {
  //$scope.title = $scope.$parent.$parent.title;

  $scope.foo = "original";
}

function RemixTrack($scope) {
  $scope.foo = "remix";
}
