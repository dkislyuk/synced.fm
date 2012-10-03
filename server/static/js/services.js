var module = angular.module('synced.services', ['ngResource']);

module.service('UserLogin', function($http) {
	this.login = function(params) {
		console.log("attempting with params: ", params);
		$http.post('/api/user/login', params).success(function(data) {
   			console.log("logged in ", data);
   		});
	};

// 	this.create = function(data) {

// 	};
});


module.factory('Track', function($resource) {
	/* If the parameter value is prefixed with @ then the value of that parameter is extracted from the data object (useful for non-GET operations). */
	return $resource('/api/track/:track_id', 
		{ track_id: '@id' }, {

	});
});

module.factory('Tag', function($resource) {
	return $resource('/api/tag/:tag_id', 
		{ tag_id: '@id' }, {

	});
});

module.factory('User', function($resource) {
	return $resource('/api/user/:username', 
		{ tag_id: '@username' }, {
	});
});