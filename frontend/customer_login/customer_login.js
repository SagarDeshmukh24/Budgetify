var app = angular.module('loginApp', []);

app.controller('LoginController', function ($scope, $http) {

  $scope.user = {};
  $scope.message = '';

  $scope.login = function () {

    $http.post('http://127.0.0.1:8000/customer/login/', {
      email: $scope.user.email,
      password: $scope.user.password
    })
    .then(function (response) {
      console.log("Login success:", response.data);

      // Store token & username
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("username", $scope.user.email);

      // Redirect to dashboard
      window.location.href = "/frontend/dashboard/dashboard.html";

    }, function (error) {
      console.error("Login failed:", error);
      $scope.message = "Invalid email or password";
    });
  };

});
