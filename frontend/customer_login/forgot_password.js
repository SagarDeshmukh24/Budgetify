var app = angular.module('forgotApp', []);

app.controller('ForgotController', function ($scope, $http) {

  $scope.user = {};
  $scope.message = '';
  $scope.error = '';

  $scope.sendOtp = function () {

    if (!$scope.user.email || !$scope.user.telegram_chat_id) {
      $scope.error = "All fields are required";
      return;
    }

    $http.post('http://127.0.0.1:8000/customer/forgot_password/', {
      email: $scope.user.email,
      telegram_chat_id: $scope.user.telegram_chat_id
    })
    .then(function (response) {
      $scope.message = response.data.message;
      $scope.error = '';
      window.location.href = "http://127.0.0.1:5500/frontend/customer_login/verify_otp.html";

    }, function (error) {
      $scope.error = error.data?.error || "Failed to send OTP";
      $scope.message = '';
    });
  };

});
