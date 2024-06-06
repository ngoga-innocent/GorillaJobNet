$(document).ready(function () {
  const url = window.location.href;
  $("#search_query").on("input", function () {
    var query = $(this).val();
    if (query.length > 3) {
      $.ajax({
        url: url,
        type: "GET",
        data: { query: query },
        success: function (data) {
          console.log(data);
          var facultyList = $("#faculty-list");
          facultyList.empty(); // Clear the existing content

          if (data.faculties.length > 0) {
            $.each(data.faculties, function (index, faculty) {
              var facultyItem =
                '<div class="rounded-lg py-2 px-2 md:w-[100%] flex flex-col w-[60%] mx-auto relative" id="faculity">' +
                '<img src="' +
                (faculty.thumbnail || "/static/images/logo.jpg") +
                '" alt="" class="w-20 h-20 rounded-full" />' +
                '<a class="hover:cursor-pointer text-white font-bold" href="/exam/' +
                faculty.id +
                '">' +
                faculty.name +
                "</a>" +
                '<div class="absolute top-2 right-1 bg-orange-200 text-white text-center rounded-md px-1">' +
                faculty.quiz_count +
                "</div>" +
                '<div class="hidden md:block"><p>' +
                faculty.description +
                "...</p></div>" +
                '<div class="absolute right-1 bottom-2 gap-x-1 flex flex-row items-center">' +
                '<a class="hover:cursor-pointer text-orange-300" href="/exam/' +
                faculty.id +
                '">View Quiz</a>' +
                '<i class="fa fa-arrow-right" style="color: white;" aria-hidden="true"></i>' +
                "</div>" +
                "</div>";
              facultyList.append(facultyItem);
            });
          } else {
            facultyList.append(
              "<p>No available Faculties please be Patient Our Team is taking care of it</p>"
            );
          }
        },
      });
    }
  });
});
$(document).ready(function (e) {
  $(".start-button").on("click", function () {
    const quizId = this.getAttribute("data-quiz-id");
    const quizName = this.getAttribute("data-quiz-name");
    const quizQuestions = this.getAttribute("data-quiz-questions");

    $.ajax({
      url: "/exam/Checkpayment",
      method: "GET",
      data: { exam_id: quizId },
      success: function (data) {
        let content;
        let header;
        let footer;
        if (!data.paid) {
          header = `Please Pay First to continue...`;
          content = `<div>
     <div class='flex flex-row gap-x-3'>
    <h5 class="text-sm text-gray-500">1 Exam :</h5>
    <p class="text-sm font-bold"> 500 Rwf</p>
    </div>

    <div class='flex flex-row gap-x-3'>
    <h5 class="text-sm text-gray-500"> Day subscription :</h5>
    <p class="text-sm  font-bold" >5000 Rwf</p>
    </div>

    <div class='flex flex-row gap-x-3'>
    <h5 class="text-sm text-gray-500"> Week Subscription :</h5>
    <p class="text-sm  font-bold"> 10000 Rwf</p>
    </div>

    <div class='flex flex-row gap-x-3'>
    <h5 class="text-sm text-gray-500"> Month Subscription :</h5>
    <p class="text-sm  font-bold"> 20000 Rwf</p>
    </div>

    

    </div>`;
          footer = `<button id="cancel"
        class="cancel px-2 py-2 rounded-md text-white font-bold bg-red-400"
      >
        Cancel
      </button>
      <button id="confirm"
        class="Pay px-4 py-2 rounded-md text-white font-bold bg-green-400"
      >
        Pay
      </button>`;
        } else {
          content = `<div>
           
                <div class='flex flex-row gap-x-3'>

    <h5 class="text-sm text-gray-500">Name:</h5>
    <p class="text-sm text-gray-500">${quizName}</p>
    </div>

    <div class='flex flex-row gap-x-3'>
    <h5 class="text-sm text-gray-500">number Question:</h5>
    <p class="text-sm text-gray-500">${quizQuestions}</p>
    </div>

    </div>`;
          footer = `<button
        class="cancel px-2 py-2 rounded-md text-white font-bold bg-red-400"
      >
        Cancel
      </button>
      <button
        class="confirm px-4 py-2 rounded-md text-white font-bold bg-green-400"
      >
        Start
      </button>`;
          header = `Are you sure you want to Start?`;
        }
        $("#modal-content").html(content);
        $("#modal-header").html(header);
        $("#modal-footer").html(footer);
        $(".modal-container").removeClass("hidden");
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
  $(document).on("click", ".cancel", function () {
    $(".modal-container").addClass("hidden");
    $("#modal-content").empty();
    $("#modal-header").empty();
    $("#modal-footer").empty();
  });

  $(document).on("click", ".confirm", function () {
    const quizId = $(".start-button").data("quiz-id");
    window.location.href = "/exam/quiz/" + quizId;
    $(".modal-container").addClass("hidden");
  });
  $(document).on("click", ".Pay", function () {
    $(".modal-container").addClass("hidden");
    $(".payment-modal").removeClass("hidden");
  });

  $(document).on("submit", "#payment_form", function (e) {
    e.preventDefault(); // Prevent the default form submission

    const formData = $(this).serialize();
    $("#loader").removeClass("hidden");
    $.ajax({
      url: "/payment/",
      method: "POST",
      data: formData,
      success: function (data) {
        console.log(data);
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});

$(document).ready(function () {
  $("#submit_question").on("click", function (e) {
    e.preventDefault();
    const questionId = this.getAttribute("data-questionId");
    const selectedAnswer = $(`input[name=${questionId}]:checked`).val();
    $.ajax({
      url: "/exam/submit",
      type: "POST",
      data: {
        answer_id: selectedAnswer,
        question_id: questionId,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        if (data.status == "success") {
          $("#next_previous").removeClass("hidden");
          $("#submit_question").addClass("hidden");
        }
      },
      error: function (e) {
        console.log(e);
      },
    });
  });
});

$(document).ready(function () {
  $("#Get_results").on("click", function (e) {
    $(".spinnerContainer").removeClass("hidden");
    url = window.location.href;

    e.preventDefault();
    const quizId = this.getAttribute("data-quizId");
    // const selectedAnswer = $(`input[name=${questionId}]:checked`).val();
    $.ajax({
      url: "/exam/get_results/" + quizId,
      type: "GET",
      // data: {
      //   answer_id: selectedAnswer,
      //   question_id: questionId,
      //   csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      // },
      success: function (data) {
        console.log(data);
        $(".spinnerContainer").addClass("hidden");
        $("#quiz_container").addClass("hidden");
        $("#results").removeClass("hidden");
        $("#results").empty();
        if (data.data.marks >= 50) {
          $("#results").append(
            `<div>
            <h2>Congratulations,</h2>
            <div id="marks_div_success" class="rounded-full w-32 h-32 bg-green-400 items-center flex flex-col justify-center text-white font-bold"> ${data.data.marks}%
            
            </div>
            <div>
            <button class='px-3 py-2 rounded-md bg-orange-300'>
            <a href="/exam/get_all_answer/${data.data.quiz_id}">View All Answer</a>
            </button>
            </div>
            </div>`
          );
        } else {
          $("#results").append(
            `<div>
            <h2>Oops!! Failed,</h2>
            <div id="marks_div_success" class="rounded-full w-32 h-32 bg-orange-400 items-center flex flex-col justify-center text-white font-bold"> ${data.data.marks}%
            
            </div>
            <div>
            <button class='px-3 py-2 rounded-md bg-orange-300'>
            <a href="/exam/get_all_answer/${data.data.quiz_id} >View All Answer</a>
            </button>
            </div>
            </div>`
          );
        }
      },
      error: function () {
        console.log("error");
      },
    });
  });
});
