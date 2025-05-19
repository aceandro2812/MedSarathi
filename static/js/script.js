document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    let chatHistory = [];

    const appendMessage = (sender, message, isTypingIndicator = false) => {
        const messageElement = document.createElement('div');
        if (isTypingIndicator) {
            messageElement.id = 'typing-indicator';
            messageElement.classList.add('mb-2', 'p-2', 'rounded-lg', 'bg-gray-200', 'text-left', 'italic');
        } else {
            messageElement.classList.add('mb-2', 'p-2', 'rounded-lg', sender === 'user' ? 'bg-blue-100' : 'bg-gray-200', sender === 'user' ? 'text-right' : 'text-left');
        }
        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to bottom
    };

    const showTypingIndicator = () => {
        appendMessage('bot', 'Bot is typing...', true);
    };

    const removeTypingIndicator = () => {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            chatContainer.removeChild(typingIndicator);
        }
    };

    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) {
            alert("Please type a message before sending."); // Simple alert for empty message
            return;
        }

        appendMessage('user', message);
        messageInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    chat_history: chatHistory
                }),
            });

            removeTypingIndicator(); // Remove typing indicator regardless of response status

            if (response.ok) {
                try {
                    const data = await response.json();
                    if (data.answer) {
                        appendMessage('bot', data.answer);
                        chatHistory.push([message, data.answer]); // Update chat history
                    } else {
                        appendMessage('bot', 'Error: Received an unexpected response from the server.');
                        console.error('Unexpected response format:', data);
                    }
                } catch (jsonError) {
                    appendMessage('bot', 'Error: Could not parse the server response.');
                    console.error('JSON parsing error:', jsonError, await response.text());
                }
            } else {
                let errorText = await response.text();
                try {
                    const errorJson = JSON.parse(errorText);
                    errorText = errorJson.detail || errorText; // Use detail from JSON if available
                } catch (e) {
                    // Not a JSON error response, use the text as is
                }
                appendMessage('bot', `Sorry, something went wrong. Please try again. (Error: ${response.status} - ${errorText})`);
                console.error('Server error:', response.status, errorText);
            }
        } catch (error) {
            removeTypingIndicator(); // Ensure indicator is removed on network error too
            appendMessage('bot', 'Sorry, something went wrong. Please try again. (Network or client-side error)');
            console.error('Fetch error:', error);
        }
    };

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
