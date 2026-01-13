var app = angular.module('otpApp', []);

app.controller('OtpController', function ($scope, $http) {

  $scope.otp = '';
  $scope.message = '';
  $scope.error = '';

  $scope.verifyOtp = function () {

    $http.post('http://127.0.0.1:8000/customer/verify_otp/', {
      otp: $scope.otp
    })
    .then(function () {
      $scope.message = "OTP verified successfully";
      $scope.error = '';
      window.location.href = "http://127.0.0.1:5500/frontend/customer_login/reset_password.html";

    }, function () {
      $scope.error = "Invalid or expired OTP";
      $scope.message = '';
    });
  };

});
