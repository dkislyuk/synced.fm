/* This module is a collection of models, which are simply RESTful resources */
var module = angular.module('synced.services', []);

module.service('GenericAPI', function($http) {
	this.get_id = function() {

	};
});

module.factory('Track', function($http) {
  // Track is a class which we can use for retrieving and
  // updating data on the server
  var Track = function(data) {
    angular.extend(this, data);
  };

  // a static method to retrieve Track by ID
  Track.get = function(id) {
    return $http.get('/api/track/' + id).then(function(response) {
      return new Track(response.data);
    });
  };

  // an instance method to create a new Track
  Track.prototype.create = function() {
    var track = this;
    return $http.post('/api/track', track).then(function(response) {
      track.id = response.data.id;
      return track;
    });
  };

  return Track;
});


module.factory('TrainingSet', function($http) {
  // Track is a class which we can use for retrieving and
  // updating data on the server
  var TrainingSet = function(data) {
    angular.extend(this, data);
  };

  // a static method to retrieve Track by ID
  TrainingSet.get = function(id) {
    return $http.get('/api/training_set/' + id).then(function(response) {
      console.log("got the response: ", response);
      return new TrainingSet(response.data);
    });
  };

  // an instance method to create a new Track
  TrainingSet.prototype.create = function() {
    var training_set = this;
    return $http.post('/api/training_set', training_set).then(function(response) {
      console.log("resp: ", response);

      training_set.id = response.data;
      return training_set;
    });
  };

  return TrainingSet;
});

