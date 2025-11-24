let currentQuestion = 0;
let questions = [];
let lastAnswerCount = 0; // ✅ Track how many gesture answers processed

function startTest() {
  document.getElementById("startBtn").style.display = "none";
  document.getElementById("questionBox").style.display = "block";

  // Add animation when test starts
  document.querySelector(".container").classList.add("test-started");

  fetch('/start_alica').then(() => {
    fetchQuestions();
  });
}

function fetchQuestions() {
  fetch('/get_questions')
    .then(res => res.json())
    .then(data => {
      questions = data.questions;
      loadQuestion();
    });
}

function loadQuestion() {
  if (currentQuestion >= questions.length) {
    fetch('/get_score')
      .then(res => res.json())
      .then(data => {
        document.getElementById("questionBox").innerHTML = `
          <div class="result-box">
            <h2>🎉 Test Completed!</h2>
            <p>Your Score: <b>${data.score}</b> / ${data.total}</p>
            <p>👏 Great effort! Try again to improve.</p>
            <button onclick="location.reload()">Restart Test</button>
          </div>
        `;
      });
    return;
  }

  const q = questions[currentQuestion];
  document.getElementById("question").innerText = `Q${currentQuestion + 1}. ${q.question}`;

  let optionsHtml = "";
  for (let key in q.options) {
    optionsHtml += `
      <div class="option-card">
        <span class="option-key">${key}</span> 
        <span class="option-text">${q.options[key]}</span>
      </div>
    `;
  }

  document.getElementById("options").innerHTML = optionsHtml;
  document.getElementById("feedback").innerHTML = `<span class="waiting">🧠 Waiting for your gesture...</span>`;
}

function handleGestureAnswer(answer) {
  const correct = questions[currentQuestion].answer;

  if (answer === correct) {
    document.getElementById("feedback").innerHTML = `<span class="correct">✅ Correct! (${answer})</span>`;
  } else {
    document.getElementById("feedback").innerHTML = `<span class="wrong">❌ Wrong! You chose ${answer}</span>`;
  }

  currentQuestion++;

  // Smooth transition before loading next question
  setTimeout(() => {
    loadQuestion();
  }, 2000);
}

// ✅ Poll Flask for new gesture answers every 1.5s
setInterval(() => {
  fetch('/get_answers')
    .then(res => res.json())
    .then(data => {
      const answers = data.answers;

      // Only respond if a new gesture is received
      if (answers.length > lastAnswerCount && currentQuestion < questions.length) {
        const newAnswer = answers[answers.length - 1];
        lastAnswerCount = answers.length;
        handleGestureAnswer(newAnswer);
      }
    });
}, 1500);
