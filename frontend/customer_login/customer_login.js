var app = angular.module('authApp', []);

app.controller('LoginController', function ($scope, $http) {

  $scope.isLogin = true; // Toggle between Login and Register
  $scope.user = {}; // Model to hold form data
  $scope.message = ''; // Message to display the status
  $scope.data = {}; // To store response data (like user data)

  // Toggle between Login and Register forms
  $scope.toggleForm = function () {
    $scope.isLogin = !$scope.isLogin; // Switch form type
    $scope.message = ''; // Reset message
    $scope.user = {}; // Clear form fields
  };

  // Handle form submission
  $scope.submitForm = function (event) {
    event.preventDefault();  // Prevent the default form submission

    console.log("Submit form triggered");

    if ($scope.isLogin) {
      // Login API Request
      $http.post('http://127.0.0.1:8000/customer/login/', {
        email: $scope.user.email,
        password: $scope.user.password
      }).then(function (response) {
        $scope.message = response.data.message; // Display login success message
        $scope.data = response.data; // Store the response data (user details)
        window.location.href = response.data.redirect_url;
        console.log(response.data);
      }, function (error) {
        $scope.message = 'Login failed'; // Handle login error
        console.error(error);
      });

    } else {
      // Register API Request (including new fields: name, phone, and type)
      $http.post('http://127.0.0.1:8000/customer/register/', {
        name: $scope.user.name,      // New field: name
        email: $scope.user.email,
        password: $scope.user.password,
        phone: $scope.user.phone,    // New field: phone
        type: $scope.user.type       // New field: type
      }).then(function (response) {
        $scope.message = response.data.message; // Display registration success message
        $scope.data = response.data;  // Store user data (response)
        console.log(response.data);   // Debug the response data
      }, function (error) {
        $scope.message = 'Registration failed'; // Handle registration error
        console.error(error);
      });
    }
  };

});
