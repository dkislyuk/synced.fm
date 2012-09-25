var module = angular.module('synced.directives', [])

module.directive('uiEvent', ['$parse',
  function($parse) {
  /* Borrowed from angular-ui, hopefully they put this into core */
    return function(scope, elm, attrs) {
      var events = scope.$eval(attrs.uiEvent);
      angular.forEach(events, function(uiEvent, eventName){
        var fn = $parse(uiEvent);
        elm.bind(eventName, function(evt) {
          var params = Array.prototype.slice.call(arguments);
          //Take out first paramater (event object);
          params = params.splice(1);
          scope.$apply(function() {
            fn(scope, {$event: evt, $params: params})
          });
        });
      });
    };
  }]
);