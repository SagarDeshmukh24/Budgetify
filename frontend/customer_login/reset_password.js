var app = angular.module('resetApp', []);

app.controller('ResetController', function ($scope, $http) {

  $scope.password = '';
  $scope.confirm = '';
  $scope.message = '';
  $scope.error = '';

  $scope.resetPassword = function () {

    if ($scope.password !== $scope.confirm) {
      return;
    }

    $http.post('http://127.0.0.1:8000/customer/reset_password/', {
      password: $scope.password
    })
    .then(function () {
      $scope.message = "Password reset successful";
      window.location.href = "http://127.0.0.1:5500/frontend/customer_login/customer_login.html";

    }, function () {
      $scope.error = "Unable to reset password";
    });
  };

});
