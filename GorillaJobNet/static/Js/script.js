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
          // console.log(data);
          var facultyList = $("#faculty-list");
          facultyList.empty(); // Clear the existing content

          if (data.faculties.length > 0) {
            $.each(data.faculties, function (index, faculty) {
              var facultyItem =
                '<div class="rounded-lg py-2 px-2 md:w-[100%] flex flex-col w-[80%] mx-auto relative" id="faculity">' +
                '<img src="' +
                (faculty.thumbnail || "/static/images/logo.jpg") +
                '" alt="" class="w-20 h-20 rounded-full" />' +
                '<a class="hover:cursor-pointer text-white max-w-[40%] text-xs font-bold" href="/exam/' +
                faculty.id +
                '">' +
                '<p class="text-xs max-w-[40%]">' +
                faculty.name +
                "</p>" +
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
                '">View Exams</a>' +
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
  // console.log("clicked clicked");
  $(".start-button").on("click", function (e) {
    e.preventDefault();
    $("#spinnerOverlay").removeClass("hidden");
    const quizId = this.getAttribute("data-quiz-id");
    const quizName = this.getAttribute("data-quiz-name");
    const quizQuestions = this.getAttribute("data-quiz-questions");

    localStorage.setItem("exam_id", quizId);
    const otp = localStorage.getItem("otp");
    $.ajax({
      url: "/exam/Checkpayment",
      method: "GET",
      data: { exam_id: quizId, otp: otp },
      success: function (data) {
        let content;
        let header;
        let footer;
        $(".spinnerOverlay").addClass("hidden");
        console.log(data.question_number);
        if (data.question_number < 1) {
          alert("This Exam has no Questions Available please Try other Exams");
        }
        if (!data.paid) {
          header = `<form class='code_check flex flex-row items-center gap-x-2'>
          <input type="number" required name="code" class='bg-slate-200 rounded-md w-[100%] rounded-md py-2 px-2' placeholder='Enter Your Code' />
          <button type='submit' class='check_code bg-[#10644D] px-3 py-2 rounded-md'><p class='text-white font-bold'>Continue</p></button>
          </form>`;
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
      <button id="confirm" data-quiz-id="${quizId}"
        class="Pay px-4 py-2 rounded-md text-white font-bold bg-[#10644D]"
      >
        Pay To Get Code
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
        class="confirm px-4 py-2 rounded-md text-white font-bold bg-[#10644D]"
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
        $(".spinnerOverlay").addClass("hidden");
        alert("error");
      },
    });
  });
  $(document).on("click", ".cancel", function () {
    $(".modal-container").addClass("hidden");
    $("#modal-content").empty();
    $("#modal-header").empty();
    $("#modal-footer").empty();
    $(".spinnerOverlay").addClass("hidden");
  });
  $(document).on("submit", ".code_check", function (e) {
    e.preventDefault();
    $(".modal-spinner").removeClass("hidden");
    const code = $(this).serialize();
    const otp = $('input[name="code"]').val();

    $.ajax({
      url: "/exam/check_otp",
      method: "GET",
      data: code,
      success: function (data) {
        $(".modal-spinner").addClass("hidden");
        if (data.valid == true) {
          const quizId = localStorage.getItem("exam_id");
          localStorage.setItem("otp", otp);
          localStorage.setItem("exam_id", quizId);
          $("#modal-message").append(
            `<p class='text-[#10644D] font-bold text-xs'>Code Validated, you will be redirect to exam page in a seconds.....</p>`
          );
          setTimeout(() => {
            window.location.href = "/exam/exam/" + quizId;
          }, 3000);
        } else {
          $("#modal-message").append(
            `<p class='text-orange-300 font-bold text-xs'>Code Provided Either Doesn't exist or Expired.....</p>`
          );
        }
      },
      error: function (error) {
        alert("error");
      },
    });
  });
  $(document).on("click", ".confirm", function () {
    const quizId = $(".start-button").data("quiz-id");
    window.location.href = "/exam/exam/" + quizId;
    $(".modal-container").addClass("hidden");
  });
  //   ///////////////////////////For The Subscription Modal
  //   // $(document).on("click", ".Pay", function () {
  //   //   $(".modal-container").addClass("hidden");
  //   //   const exam_id = this.getAttribute("data-quiz-id");
  //   //   // alert(exam_id);
  //   //   $(".payment-modal").removeClass("hidden");
  //   // });
  $(document).on("click", ".cancel", function () {
    $(".modal-container").addClass("hidden");
  });
  $(document).on("click", ".Pay", function () {
    $(".modal-container").addClass("hidden");
    const exam_id = this.getAttribute("data-quiz-id");
    // alert(exam_id);
    $(".quiz-payment-modal").removeClass("hidden");

    $(document).on("submit", "#quiz_payment_form", function (e) {
      e.preventDefault(); // Prevent the default form submission
      $("#exam_id").val(exam_id);
      const formData = $(this).serialize();
      // alert("form submitted");
      $("#loader1").removeClass("hidden");
      $.ajax({
        url: "/payment/",
        method: "POST",
        data: formData,
        success: function (data) {
          CheckPaymentStatusSingle(data.ref, data.phone, exam_id, data.otp);
          // console.log(data);
        },
        error: function (error) {
          alert("error");
        },
      });
    });
  });

  $(document).on("submit", "#payment_form", function (e) {
    e.preventDefault(); // Prevent the default form submission
    $("#loader").removeClass("hidden");
    $("#payment_buttons").addClass("hidden");
    const formData = $(this).serialize();

    $.ajax({
      url: "/payment/",
      method: "POST",
      data: formData,
      success: function (data) {
        CheckPaymentStatus(data.ref, data.phone, data.otp);
        // console.log(data);
      },
      error: function (error) {
        alert("error");
      },
    });
  });
  function CheckPaymentStatusSingle(ref, phone, exam_id, otp) {
    const interval = setInterval(() => {
      $.ajax({
        url: "/payment/payment_status",
        method: "GET",
        data: { ref: ref, phone: phone, otp: otp },
        success: function (data) {
          if (data.status == "success") {
            clearInterval(interval);
            $("#loader").addClass("hidden");
            $("#message_modal1").removeClass("hidden");
            $("#message_modal1").addClass("bg-red-400");
            $("#message_modal1").html(
              `<div class='min-h-screen w-full flex flex-col items-center justify-center absolute top-0' style='z-index-9999999;width:"400px"; background-color:rgba(0,0,0,0.8)'>
              <div class='z-50 bg-white px-2 py-2 rounded-md' style='z-index:99999999'>
              <p class='text-[#10644D] font-bold text-xs'>Congratulations,Payment Successfully Completed </p>
              <p>Copy Your Entrance code to Safe Place </p>
              <div class='flex flex-row gap-x-3 items-center'>
              <input type="text" class='bg-white px-2 py-2 rounded-md' value=${data.otp} id="myInput">

              <button id="copy_code" class='bg-[#10644D] rounded-md px-2 py-2' onclick="copyCode()">Copy Code</button>
              <a href="/exam/exam/${exam_id}" class='text-white text-xs font-bold py-2 px-4 bg-[#10644D] rounded-md '>Explore the Exam</a>
              </div>
              </div>
              </div>`
            );
            // setTimeout(() => {
            //   window.location.href = "/exam/exam/" + exam_id;
            // }, 5000);
          } else if (data.status === "failed") {
            clearInterval(interval);
            $("#loader").addClass("hidden");
            $("#message_modal1").removeClass("hidden");
            $("#message_modal1").addClass("bg-red-400");
            $("#message_modal1").html(`Payment Failed Please try again`);
            setTimeout(() => {
              window.location.href = "/exam/";
            }, 5000);
          }
        },
        error: function (error) {
          alert("error");
        },
      });
    }, 2000);
  }
  function CheckPaymentStatus(ref, phone, otp) {
    const interval = setInterval(() => {
      $.ajax({
        url: "/payment/payment_status",
        method: "GET",
        data: { ref: ref, phone: phone, otp: otp },
        success: function (data) {
          if (data.status == "success") {
            clearInterval(interval);
            $("#loader").addClass("hidden");
            $("#message_modal").removeClass("hidden");
            // $("#message_modal").addClass("bg-green-400");
            $("#message_modal").html(
              `<div class='z-50 bg-white'>
              <p class='text-[#10644D] font-bold text-xs'>Congratulations,Payment Successfully Completed </p>
              <p>Copy Your Entrance code to Safe Place </p>
              <div class='flex flex-row gap-x-3 items-center'>
              <input type="text" class='bg-white px-2 py-2 rounded-md' value=${data.otp} id="myInput">

              <button id="copy_code" class='bg-[#10644D] rounded-md px-2 py-2' onclick="copyCode()">Copy Code</button>

              </div>
            <a href="/exam/" class='text-white font-bold py-2 px-4 bg-[#10644D] rounded-md '>Explore the Exam</a>
              </div>`
            );
            setTimeout(() => {
              window.location.href = "/";
            }, 5000000);
          } else if (data.status === "failed") {
            clearInterval(interval);
            $("#loader").addClass("hidden");
            $("#message_modal").removeClass("hidden");
            $("#message_modal").addClass("bg-red-400");
            $("#message_modal").html(
              `<p class="text-white">Payment Failed  </p>`
            );
            setTimeout(() => {
              window.location.href = "/";
            }, 5000);
          }
        },
        error: function (error) {
          alert("error");
          clearInterval(interval);
          $("#loader").addClass("hidden");
          $("#message_modal").removeClass("hidden");
          $("#message_modal").addClass("bg-red-400");
          $("#message_modal").html(
            `<p class="text-white">Payment Failed  </p>`
          );
          setTimeout(() => {
            window.location.href = "/";
          }, 5000);
        },
      });
    }, 2000);
  }
});
$(document).ready(function () {
  $(document).on("click", "#copy_code", function (e) {
    var copyText = document.getElementById("myInput");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Copied the text: " + copyText.value);
  });
});
$(document).ready(function () {
  let current_page = 1;
  $("#quiz_container").on("submit", function (e) {
    e.preventDefault();
    form_value = $(this).serialize();

    const answerId = $('input[name="question_radio"]:checked').val();
    const questionId = $("#question_id").val();
    const examId = localStorage.getItem("exam_id");
    const otp = localStorage.getItem("otp");

    $(".spinnerContainer").removeClass("hidden");
    reloadCsrfToken(function (token) {
      $.ajax({
        url: "/exam/exam/" + examId,
        type: "POST",
        data: {
          answer_id: answerId,
          question_id: questionId,
          code: otp,
          question_number: current_page,
          csrfmiddlewaretoken: token,
        },
        success: function (data) {
          console.log(data);
          if (data.status == "success") {
            $(".spinnerContainer").addClass("hidden");

            console.log(data.has_next == true);
            // Update the question container with new question data
            $("#quiz_container").html(data.html);
            current_page++;
          }
          if (data.marks >= 0) {
            $(".spinnerContainer").addClass("hidden");
            console.log(data.marks);
            $("#results").append(`<div>
            <p class='my-2 font-bold'>Here Is Your Marks</p>
            <div class="rounded-full w-32 h-32 flex flex-col items-center justify-center bg-slate-400">
            ${data.marks}%
            </div>
            <a href='/exam/get_all_answer' class='bg-[#10644D] px-4 py-2 rounded-md'> Check The Answers</a>
            </div>`);
            $("#quiz_container").addClass("hidden");
            $("#results").removeClass("hidden");
          }
          if (data.reject_message) {
            $(".spinnerContainer").addClass("hidden");
            $("#quiz_container").addClass("hidden");
            $("#results").append(`<div>
           
            <div class=" flex flex-col items-center justify-center bg-slate-400 px-4 rounded-md">
            <p class='text-orange-200'>${data.reject_message}</p>
            </div>
            </div>`);
            $("#results").removeClass("hidden");
          }
        },
        error: function (e) {
          alert(e);
          $(".spinnerContainer").addClass("hidden");
        },
      });
    });
  });

  function reloadCsrfToken(callback) {
    $.get("/exam/csrf_token/", function (data) {
      // Call the callback function with the new token value
      callback(data.token);
    });
  }
});

// function SubmitAnswer(question_id, answer_id) {
//   $("#submit_question").on("click", function (e) {
//     e.preventDefault();
//     const questionId = this.getAttribute("data-questionId");
//     //const selectedAnswer = $(`input[name=${questionId}]:checked`).val();
//     const otp = localStorage.getItem("otp");
//     // console.log(otp);
//     $.ajax({
//       url: "/exam/submit",
//       type: "POST",
//       data: {
//         answer_id: question_id,
//         question_id: answer_id,
//         code: otp,
//         csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
//       },
//       success: function (data) {
//         if (data.status == "success") {
//           $("#next_previous").removeClass("hidden");
//           $("#submit_question").addClass("hidden");
//         }
//       },
//       error: function (e) {
//         console.log(e);
//       },
//     });
//   });
// }

$(document).ready(function () {
  $("#Get_results").on("click", function (e) {
    $(".spinnerContainer").removeClass("hidden");
    url = window.location.href;

    e.preventDefault();
    // const quizId = this.getAttribute("data-quizId");
    const quizId = localStorage.getItem("exam_id");
    // const selectedAnswer = $(`input[name=${questionId}]:checked`).val();
    $.ajax({
      url: "/exam/get_results/" + quizId,
      type: "GET",
      data: {
        otp: localStorage.getItem("otp"),
      },
      success: function (data) {
        // console.log(data);
        $(".spinnerContainer").addClass("hidden");
        $("#quiz_container").addClass("hidden");
        $("#results").removeClass("hidden");
        $("#results").empty();
        if (data.marks >= 50) {
          $("#results").append(
            `<div>
            <h2>Congratulations,</h2>
            <div id="marks_div_success" class="rounded-full w-32 h-32 bg-green-400 items-center flex flex-col justify-center text-white font-bold"> ${data.marks}%
            
            </div>
            <div>
            <button class='px-3 py-2 rounded-md bg-orange-300'>
            <a href="/exam/get_all_answer/${data.quiz_id}">View All Answer</a>
            </button>
            </div>
            </div>`
          );
        } else {
          $("#results").append(
            `<div>
            <h2>Oops!! Failed,</h2>
            <div id="marks_div_success" class="rounded-full w-32 h-32 bg-orange-400 items-center flex flex-col justify-center text-white font-bold"> ${data.marks}%
            
            </div>
            <div>
            <button class='px-3 py-2 rounded-md bg-orange-300'>
            <a href="/exam/get_all_answer/${data.quiz_id}" >View All Answer</a>
            </button>
            </div>
            </div>`
          );
        }
      },
      error: function () {
        alert("error");
      },
    });
  });
});
//////////////////payments////////////////
$(document).ready(function () {
  $("#Subscription").on("click", function () {
    $(".payment-modal").removeClass("hidden");
  });
  $("#cancel_pay_Button").on("click", function () {
    $(".payment-modal").addClass("hidden");
  });
});
