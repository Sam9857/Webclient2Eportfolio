// Small extras. The site still works without JavaScript.


// 1. "Are you sure?" before deleting something
var deleteForms = document.querySelectorAll("form[data-confirm]");
for (var i = 0; i < deleteForms.length; i++) {
  deleteForms[i].addEventListener("submit", function (event) {
    if (!confirm(this.getAttribute("data-confirm"))) {
      event.preventDefault();
    }
  });
}


// 2. Quiz setup page: show the number next to the slider
var slider = document.getElementById("num-questions");
if (slider) {
  var sliderNumber = document.getElementById("num-value");
  sliderNumber.textContent = slider.value;
  slider.addEventListener("input", function () {
    sliderNumber.textContent = slider.value;
  });
}


// 3. Quiz page: highlight the chosen option and update the progress bar
var quizForm = document.getElementById("quiz-form");
if (quizForm) {
  var totalQuestions = quizForm.querySelectorAll(".question").length;

  quizForm.addEventListener("change", function (event) {
    // remove the highlight from the other options of this question
    var question = event.target.closest(".question");
    var options = question.querySelectorAll(".option");
    for (var i = 0; i < options.length; i++) {
      options[i].classList.remove("selected");
    }
    event.target.closest(".option").classList.add("selected");

    // update the counter and the bar
    var answered = quizForm.querySelectorAll("input[type=radio]:checked").length;
    document.getElementById("answered-count").textContent = answered + " of " + totalQuestions + " answered";
    document.getElementById("progress-fill").style.width = (answered / totalQuestions * 100) + "%";
  });
}
