var app = angular.module('registerApp', []);

app.controller('RegisterController', function ($scope, $http) {

  $scope.user = {};
  $scope.message = '';

  $scope.passwordMatched = false;
  $scope.passwordStatus = '';

  // Check password match
  $scope.checkPassword = function () {
    if (!$scope.user.password || !$scope.user.repassword) {
      $scope.passwordStatus = '';
      $scope.passwordMatched = false;
      return;
    }

    if ($scope.user.password === $scope.user.repassword) {
      $scope.passwordStatus = 'password matched';
      $scope.passwordMatched = true;
    } else {
      $scope.passwordStatus = 'password not matching';
      $scope.passwordMatched = false;
    }
  };

  // Register customer
  $scope.register = function () {

    if (!$scope.passwordMatched) {
      return;
    }

    $http.post('http://127.0.0.1:8000/customer/register/', {
      name: $scope.user.name,
      email: $scope.user.email,
      password: $scope.user.password,
      phone: $scope.user.phone,
      type: 'customer'
    })
    .then(function (response) {
      console.log("Registration success:", response.data);
      $scope.message = response.data.message;

      // Redirect to login page
      setTimeout(function () {
        window.location.href = "http://127.0.0.1:5500/frontend/customer_login/customer_login.html";
      }, 1500);

    }, function (error) {
      console.error("Registration failed:", error);
      $scope.message = "Registration failed. Please try again.";
    });
  };

});
