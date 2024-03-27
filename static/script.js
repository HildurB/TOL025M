function sendMessageToServer(userInput) {
    var chatBox = document.getElementById("chat-box");
    var userMessage = "<p><strong>You:</strong> " + userInput + "</p>";
    chatBox.innerHTML += userMessage;

    // Send the user input to the server
    fetch("/send-message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        var aiMessage = "<p><strong>Weatherwizard:</strong> " + data.message + "</p>";
        chatBox.innerHTML += aiMessage;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
    })
    .catch(error => console.error('Error:', error));

    document.getElementById("user-input").value = ""; // Clear input field
    document.getElementById("example-questions").style.display = "none";
}

function sendMessage() {
  var userInput = document.getElementById("user-input").value;
  if (userInput.trim() === "") return;
  sendMessageToServer(userInput);
}

function sendMessageEx1() {
    sendMessageToServer("How is the weather in New York?");
}

function sendMessageEx2() {
    sendMessageToServer("How is the temperature tomorrow in Berlin, can you give it hourly?");
}

function sendMessageEx3() {
    sendMessageToServer("ow is the weather this week in London?");
}

function sendMessageEx4() {
    sendMessageToServer("How is the weather in Dubai the day after tomorrow?");
}


