var module = angular.module('synced.services', ['ngResource']);

// module.service('Track', function($http) {
// 	this.get = function(id) {

// 	};

// 	this.create = function(data) {

// 	};
// });


module.factory('Track', function($resource) {
	/* If the parameter value is prefixed with @ then the value of that parameter is extracted from the data object (useful for non-GET operations). */
	return $resource('/api/track/:track_id.json', 
		{ track_id: '@id' }, {
		// action1: {method:?, params:?, isArray:?}, 
		// create: {method: 'POST'},
		clever_action: {method: 'POST', params: {some_id: 'some_value'}, isArray: true}
	});
});


// 	// return {


// 	// 	func1: function(param) {
// 	// 		return "hello " + param;
// 	// 	},
// 	// 	func2: function(param) {
// 	// 		return "asdlfjaslkj " + param;
// 	// 	}
// 	// }
// });

