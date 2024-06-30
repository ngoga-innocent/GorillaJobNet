$(document).ready(function () {
  $(".post_announcements_modal_button").on("click", function () {
    $("#announcement_spinner").removeClass("hidden");
    $.ajax({
      url: "/announcements/check_ann",
      method: "GET",
      success: function (data) {
        if (data.success) {
          $("#post_announcement_modal").removeClass("hidden");
          $("#announcement_spinner").addClass("hidden");
        } else {
          $("#announcement_pay_modal").removeClass("hidden");
          $("#announcement_spinner").addClass("hidden");
        }
      },
      error: function (e) {
        console.log(e);
        alert("Error Please Check your Internet connection and try again");
      },
    });
  });
  $("#close_post_announcemnt_modal").on("click", function () {
    $("#post_announcement_modal").addClass("hidden");
  });
  $("#cancel_ann_pay_modal").on("click", function () {
    $("#announcement_pay_modal").addClass("hidden");
  });
  $("#announcement_payment_form").on("submit", function (e) {
    e.preventDefault();
    $("#pay_spinner").removeClass("hidden");
    $.ajax({
      url: "/announcements/pay_announc",
      method: "POST",

      data: {
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        name: $('input[name="name"]').val(),
        age: $('input[name="age"]').val(),
        phone: $('input[name="phone"]').val(),
      },

      success: function (data) {
        console.log(data);

        setInterval(() => {
          CheckAnnouncementPaid(data.refrenceKey, data.phone, data.otp);
        }, 2000);
      },
      error: function (e) {
        console.log(e);
        alert("Error Please Check your Internet connection and try again");
      },
    });
  });
});
function CheckAnnouncementPaid(refrenceKey, phone, otp) {
  $.ajax({
    url: "/announcements/check_announc_paid",
    method: "GET",
    data: {
      ref: refrenceKey,
      phone: phone,
      otp: otp,
    },
    success: function (data) {
      console.log(data);
      if (data.success == true) {
        $("#otp_box").html(
          `<h2 class='text-[#10644D] font-bold'> Your OTP is ${otp} </h2>`
        );
        $("#pay_spinner").addClass("hidden");
        setTimeout(() => {
          $("#announcement_pay_modal").addClass("hidden");
          $("#post_announcement_modal").removeClass("hidden");
        }, 50000);

        localStorage.setItem("otp", otp);
      } else if (data.status == "failed") {
        setTimeout(() => {
          alert("payment Failed");
          window.location.href = "/announcements";
        }, 5000);
      }
    },
    error: function (e) {
      console.log(e);
      alert("Error Please Check your Internet connection and try again");
    },
  });
}

$(document).ready(function () {
  $(".category_button").on("click", function () {
    const category_id = $(this).attr("data-id");
    $.ajax({
      url: "/announcements/" + category_id,
      method: "GET",
      success: function (data) {
        // console.log(data.html);
        $("#announcements-container").html(data.html);
      },
      error: function (e) {
        console.log(e);
        alert("Error Please Check your Internet connection and try again");
      },
    });
  });
});

$(document).ready(function () {
  $("#search_announcement_form").on("submit", function (e) {
    e.preventDefault();
    const search_text = $("#search_announcement").val();
    if (search_text) {
      console.log(search_text);
      $.ajax({
        url: "/announcements/search/" + search_text,
        method: "GET",
        success: function (data) {
          // console.log(data.html);
          $("#announcements-container").html(data.html);
        },
        error: function (e) {
          console.log(e);
          alert("Error Please Check your Internet connection and try again");
        },
      });
      return false;
    } else {
      location.reload();
    }
  });
});
$(document).ready(function () {
  $("#check_otp_announcement").on("submit", function (e) {
    e.preventDefault();
    var otp = $('input[name="otp"]').val();
    $.ajax({
      url: "/announcements/check_otp",
      method: "POST",
      data: {
        otp: otp,
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      },
      success: function (data) {
        console.log(data);
        if (data.valid) {
          $("#announcement_pay_modal").addClass("hidden");
          $("#post_announcement_modal").removeClass("hidden");
        } else {
          $("#message_box").html(
            '<h2 class="text-[#10644D] text-bold">Invalid Otp</h2>'
          );
        }
      },
      error: function (xhr, status, error) {
        alert("Error");
      },
    });
    return false; // to prevent form from submitting
  });
});
