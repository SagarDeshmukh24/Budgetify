var token = localStorage.getItem("token");

if (!token) {
    window.location.href = "http://127.0.0.1:5500/frontend/login/login.html";
}
var app = angular.module("myApp", []);

app.controller("DashboardCtrl", function ($scope) {

    // localStorage.setItem("token", response.data.token); //token liya hai kyu ki aise hi koi dashboard use na kre 
    // localStorage.setItem("username", response.data.username);

    if (!localStorage.getItem("token")) {   // ye token use kiya hai kyu ki aise hi koi dashboard use na kre 
      sessionStorage.clear()
    window.location.href = "http://127.0.0.1:5500/frontend/login/login.html";
}

    $scope.username = localStorage.getItem("username");

//LOGOUT FUNCTION

    $scope.logout = function () {
  localStorage.clear();   // ya sessionStorage.clear()
  window.location.href = "http://127.0.0.1:5500/frontend/login/login.html";
};

  // TEMP STATIC DATA (backend abhi nahi)
  $scope.totalIncome = 30000;
  $scope.totalExpense = 12000;
  $scope.savings = $scope.totalIncome - $scope.totalExpense;

  $scope.recentTransactions = [
    { type: "Income", amount: 15000, description: "Salary" },
    { type: "Expense", amount: 500, description: "Food" },
    { type: "Expense", amount: 2000, description: "Shopping" },
    { type: "Income", amount: 15000, description: "Freelance" }
  ];

});


