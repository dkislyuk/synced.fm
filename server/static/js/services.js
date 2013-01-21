/* This module is a collection of models, which are simply RESTful resources */
var module = angular.module('synced.services', []);

module.service('GenericAPI', function($http) {
	this.get_id = function() {

	};
});

module.factory('Track', function($http) {
  // Book is a class which we can use for retrieving and
  // updating data on the server
  var Track = function(data) {
    angular.extend(this, data);
  };

  // a static method to retrieve Book by ID
  Track.get = function(id) {
    return $http.get('/api/track/' + id).then(function(response) {
      return new Track(response.data);
    });
  };

  // an instance method to create a new Book
  Track.prototype.create = function() {
    var book = this;
    return $http.post('/api/track', book).then(function(response) {
      book.id = response.data.id;
      return book;
    });
  };

  return Track;
});
