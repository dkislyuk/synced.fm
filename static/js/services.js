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
		// action1: {method:?, params:?, isArray:?}, 
		// create: {method: 'POST'},
		clever_action: {method: 'POST', params: {some_id: 'some_value'}, isArray: true}
	});
});

// module.factory('Track', function($resource) {
//   $resource.url('/api/track/:track_id', {
//     track_id : '@id',
//   },{
//     query : 	{ method : 'GET', isArray : true },
//     save : 		{ method : 'PUT' }, /* Update method */
//     create : 	{ method : 'POST' },
//     destroy : 	{ method : 'DELETE' }
//   })
// });


//module.factory('Track', function($http) {

// 	// return {


// 	// 	func1: function(param) {
// 	// 		return "hello " + param;
// 	// 	},
// 	// 	func2: function(param) {
// 	// 		return "asdlfjaslkj " + param;
// 	// 	}
// 	// }
// });
//});

