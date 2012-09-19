var module = angular.module('synced.services', ['ngResource']);

// module.service('Track', function($http) {
// 	this.get = function(id) {

// 	};

// 	this.create = function(data) {

// 	};
// });


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