var app = angular.module('synced', ['synced.auth', 'synced.services', 'synced.directives']);
  
app.config(['$routeProvider','$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true),
    $routeProvider.
      /* Track routing */
      when('/track/new',         { templateUrl: '/static/views/track/new.html',   controller: TrackFormsController}).
      when('/track/:track_id',   { templateUrl: '/static/views/track/index.html', controller: TrackController}).

      /* Tag routing */
      //when('/tag/new',           { templateUrl: '/static/views/track/new.html',   controller: TrackFormsController}).
      when('/track/:tag_id',     { templateUrl: '/static/views/track/index.html', controller: TrackController}).

      /* User routing */
      when('/signup',            { templateUrl: '/static/views/user/new.html',    controller: UserSignupController}).

      /* Training */
      when('/training/new',      { templateUrl: '/static/views/training/new.html', controller: TrackController}).
      when('/training/:train_id',{ templateUrl: '/static/views/training/index.html', controller: TrackController}).


      /* Authentication */
      when('/login',             { templateUrl: '/static/views/user/login.html'}).
      otherwise({redirectTo: '/track/new'});
}]);

app.run(function(userService) {
  /* Attempt to log in user */
  userService.status();
});
