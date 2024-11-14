$('#reg_form').on('submit', function (event) {
    event.preventDefault();
    var username = $('#username').val();
    var name = $('#name').val();
    var surname = $('#surname').val();
    var password = $('#password').val();
    var r_password = $('#r_password').val();
    var birth_date = $('#birth_date').val();
    console.log("Username: " + username);
    console.log("Name: " + name);
    console.log("Surname: " + surname);
    console.log("Password: " + password);
    console.log("Repeated password: " + r_password);
    console.log("Birth date: " + birth_date);
    $.ajax({
        url: "{% url 'registration' %}",
        method: 'POST',
        data: {
            username: username,
            name: name,
            surname: surname,
            password: password,
            r_password: r_password,
            birth_date: birth_date
        },
        success: function(response) {
          console.log('Success:', response);
        },
        error: function(error) {
          console.error('Error:', error);
        }
    });
});