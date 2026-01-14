var app = angular.module('forgotApp', []);

app.controller('ForgotController', function ($scope, $http, $timeout) {

  // 0 = forgot, 1 = verify otp, 2 = reset
  $scope.step = 0;

  $scope.user = {};
  $scope.otp = '';
  $scope.password = '';
  $scope.confirm = '';

  $scope.message = '';
  $scope.error = '';

  /* ================= SEND OTP ================= */
  $scope.sendOtp = function () {

    $scope.message = '';
    $scope.error = '';

    if (!$scope.user.email || !$scope.user.telegram_chat_id) {
      $scope.error = "All fields are required";
      return;
    }

    $http.post('http://127.0.0.1:8000/customer/forgot_password/', {
      email: $scope.user.email,
      telegram_chat_id: $scope.user.telegram_chat_id
    })
    .then(function (response) {

      $scope.message = response.data.message || "OTP sent successfully";

      $timeout(function () {
        $scope.step = 1;   // 🔥 SLIDE TO OTP
        $scope.message = '';
      }, 700);

    }, function (error) {
      $scope.error = error.data?.error || "Failed to send OTP";
    });
  };

  /* ================= VERIFY OTP ================= */
  $scope.verifyOtp = function () {

    $scope.message = '';
    $scope.error = '';

    $http.post('http://127.0.0.1:8000/customer/verify_otp/', {
      otp: $scope.otp
    })
    .then(function () {

      $scope.message = "OTP verified successfully";

      $timeout(function () {
        $scope.step = 2;   // 🔥 SLIDE TO RESET
        $scope.message = '';
      }, 500);

    }, function () {
      $scope.error = "Invalid or expired OTP";
    });
  };

  /* ================= RESET PASSWORD ================= */
  $scope.resetPassword = function () {

    $scope.message = '';
    $scope.error = '';

    if ($scope.password !== $scope.confirm) {
      return;
    }

    $http.post('http://127.0.0.1:8000/customer/reset_password/', {
      password: $scope.password
    })
    .then(function () {

      $scope.message = "Password reset successful";

      $timeout(function () {
        window.location.href =
          "http://127.0.0.1:5500/frontend/customer_login/customer_login.html";
      }, 1000);

    }, function () {
      $scope.error = "Unable to reset password";
    });
  };

});
