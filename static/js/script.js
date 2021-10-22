$("#id_muscle_group").change(function () {
    var url = $("#workoutItemForm").attr("data-exercises-url");  // get the url of the `load_exercises` view
    var mg_Id = $(this).val();  // get the selected muscle_group ID from the HTML input

    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request 
      data: {
        'muscle_group': mg_Id       // add the muscle_group id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_exercises` view function
        $("#id_exercise").html(data);  // replace the contents of the exercise input with the data that came from the server
      }
    });

  });