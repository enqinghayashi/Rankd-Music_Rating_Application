document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.nav-protected').forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var loginAccount = new bootstrap.Modal(document.getElementById('loginAccount'));
      loginAccount.show();
    });
  });
});