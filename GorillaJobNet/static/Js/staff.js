$(document).ready(function () {
  $.ajax({
    url: "/staff/fetch_faculties",
    method: "GET",
    success: function (data) {
      var selectBox = $("#mySelectBox");
      selectBox.empty(); // Clear existing options
      selectBox.append('<option value="">Select an item</option>');
      $.each(data, function (index, item) {
        selectBox.append(
          '<option value="' + item.id + '">' + item.name + "</option>"
        );
      });
    },
    error: function (xhr, status, error) {
      alert("Unknown Error");
    },
  });
  $("#add_exam_button").on("click", function () {
    $(".exam_modal").removeClass("hidden");
  });
  $("#mySelectBox").on("change", function () {
    var selectedValue = $(this).val();
  });
  //hiding modal
  $("#close_modal").on("click", function () {
    $(".exam_modal").addClass("hidden");
  });

  ////////////////////////Submitting exam form //////////////////////////
  $("#exam_form").on("submit", function (e) {
    e.preventDefault(); // Prevent the default form submission
    const formData = $(this).serialize();
    $("#loader2").removeClass("hidden");
    $.ajax({
      url: "/staff/exam",
      method: "POST",
      data: formData,
      success: function (data) {
        // console.log(data);
        if (data.status == true) {
          localStorage.setItem("exam_id", data.exam_id);
          $("#message_modal2").removeClass("hidden");
          $("#message_modal2").addClass("bg-green-300");

          $("#message_modal2").html(`<p>Exam Submitted Successsfully</p>`);
          setTimeout(() => {
            window.location.href = "/staff/add_questions";
          }, 5000);
        } else {
          $("#message_modal2").removeClass("hidden");
          $("#message_modal2").addClass("bg-red-300");
          $("#message_modal2").html(
            `<p class="text-white">` + data.message + `</p>`
          );
          setTimeout(() => {
            window.location.reload();
          }, 5000);
        }
      },
      error: function (xhr, status, error) {
        alert("Error");
      },
    });
  });
});

///////// ON question page ///////////////
$(document).ready(function () {
  // Check if on the add question page
  if (window.location.pathname === "/staff/add_questions") {
    var examId = localStorage.getItem("exam_id");
    if (examId) {
      $.ajax({
        url: "/staff/get_quiz",
        method: "GET",
        data: { exam_id: examId },
        success: function (data) {
          if (data.status == "success") {
            // console.log(data);
            // Update the page with exam details
            $("#exam_name").text(
              `Add Questions and Answer for ${data.exam.name}`
            );
            getQuestions();
            // $("#exam_description").text(data.exam.description);
            // You can add more fields as needed
          } else {
            alert("Error fetching exam details");
          }
        },
        error: function (xhr, status, error) {
          alert("Unkown Error");
        },
      });
    } else {
      alert("No exam found");
    }
  }
});
// $(document).ready(function () {
//   $("#add_option").on("click", function () {
//     alert("Please enter");
//     const option_number = $(".option").length + 1;
//     $(".option_container").append(
//       `<div class="items-center flex flex-row gap-x-2 option-group">
//           <input
//             type="text"
//             name="option"
//             class="bg-white shadow-sm shadow-black py-2 px-2 w-[90%] rounded-md"
//             placeholder="Add Option 4"
//           />
//           <input
//             type="checkbox"
//             name="correct_option"
//             class="bg-white w-7 h-7 roounded-sm"
//           />
//         </div>`
//     );
//   });
// });
$(document).ready(function () {
  $("#add_option").on("click", function () {
    const option_number = $(".option-group").length + 1;
    $("#answer_input").append(
      `<div class="items-center flex flex-row gap-x-2 option-group">
          <input
            type="text"
            name="option"
            class="bg-white shadow-sm shadow-black py-2 px-2 w-[90%] rounded-md"
            placeholder="Add Option ${option_number}"
            
          />
          <input
            type="checkbox"
            name="correct_option"
            class="bg-white w-7 h-7 roounded-sm"
          />
        </div>`
    );
  });
  $("#questions").on("submit", function (e) {
    e.preventDefault();
    $(".submit_question_loaded").removeClass("hidden");
    const options = [];
    var examId = localStorage.getItem("exam_id");
    $(".option-group").each(function () {
      const optionText = $(this).find('input[type="text"]').val();
      const isCorrect = $(this).find('input[type="checkbox"]').is(":checked");
      if (optionText.trim() !== "") {
        options.push({ text: optionText, correct: isCorrect });
      }
    });
    // console.log(options);
    const data = {
      question_text: $('input[name="question"]').val(),
      options: options,
    };
    $.ajax({
      url: "/staff/add_questions",
      method: "POST",
      data: {
        exam_id: examId,
        data: JSON.stringify(data),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (data) {
        $("#questions")[0].reset();
        getQuestions();
        $(".submit_question_loaded").addClass("hidden");
      },
      error: function (xhr, status, error) {
        alert("Error");
      },
    });
  });
});

function getQuestions() {
  quizId = localStorage.getItem("exam_id");
  $("#quiz_question_container").empty();
  $.ajax({
    url: "/staff/get_quiz_questions",
    method: "GET",
    data: { exam_id: quizId },
    success: function (data) {
      const questions = data.questions;
      if (questions.length > 0) {
        questions.forEach((question) => {
          let optionsHtml = "";
          question.options.forEach((option) => {
            optionsHtml += `<div class="mx-4">
                ${option.text} ${option.correct ? "(Correct)" : ""}
              </div>`;
          });
          $("#quiz_question_container").append(`
              <div class="gap-1">
                <h2 class="font-bold">${question.text}</h2>
                ${optionsHtml}

                <button type="button" class="delete_question_btn" data-quiz-id="${question.id}">Delete</button>
              </div>
              
            `);
        });
      }
    },
    error: function (xhr, status, error) {
      alert("Error");
    },
  });
}
$(document).on("click", ".delete_question_btn", function (e) {
  e.preventDefault();
  const quizId = $(this).data("quiz-id");
  // console.log("quizId");
  $.ajax({
    url: "/staff/delete_question",
    method: "POST",
    data: { quiz_id: quizId },
    success: function (data) {
      // console.log(data);
      if (data.status == "success") {
        getQuestions();
      }
    },
    error: function (xhr, status, error) {
      alert("Error ");
    },
  });
});
$(document).ready(function () {
  $(".quiz_button_edit").on("click", function (e) {
    e.preventDefault();
    const exam_id = $(this).data("quiz-id");
    // alert(exam_id);
    localStorage.setItem("exam_id", exam_id);
    window.location.href = "/staff/add_questions";
  });
});
$("#add_faculity_button").on("click", function () {
  $(".faculity_modal").removeClass("hidden");
});
$(document).on("click", "#close_modal_faculity", function () {
  $(".faculity_modal").addClass("hidden");
});
$("#faculity_form").on("submit", function (e) {
  e.preventDefault(); // Prevent the default form submission
  const formData = $(this).serialize();
  $("#loader3").removeClass("hidden");
  $.ajax({
    url: "/staff/faculity",
    method: "POST",
    data: formData,
    success: function (data) {
      // console.log(data);
      if (data.status == true) {
        $("#message_modal3").removeClass("hidden");
        $("#message_modal3").addClass("bg-green-300");
        $("#message_modal3").html(
          `<div class="">Faculity Created Successfully</div>`
        );
        window.location.reload();
      } else {
        $("#message_modal3").removeClass("hidden");
        $("#message_modal3").addClass("bg-red-300");
        $("#message_modal3").html(
          `<div class="">Failed to create a Faculity</div>`
        );
        window.location.reload();
      }
    },
    error: function (xhr, status, error) {
      alert("Error Occured");
    },
  });
});
$(document).on("click", ".faculityDelete", function (e) {
  e.preventDefault();
  const faculity_id = $(this).data("faculity-id");
  // console.log("Delete Button Clicked, ID:", faculity_id);
  const confirmation = confirm("Are you sure you want to delete this faculty?");
  if (confirmation) {
    $.ajax({
      url: "/staff/delete_fuculity",
      method: "GET",
      data: { faculity_id: faculity_id },
      success: function (data) {
        if (data.status == true) {
          alert("Faculty Deleted Successfully");
        } else {
          alert("Failed to delete Faculty");
        }
        window.location.reload();
      },
      error: function (xhr, status, error) {
        alert("Error deleting Faculty");
        window.location.reload();
      },
    });
  }
});
