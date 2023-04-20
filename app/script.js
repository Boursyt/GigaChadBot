document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    const userInput = document.querySelector('#user_input').value;
    fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({user_input: userInput})
    })
    .then(response => response.json())
    .then(data => {
      const chatbotResponse = document.querySelector('#chatbot-response');
      chatbotResponse.innerHTML = `Chatbot: ${data.best_response}`;
    });
  });
  