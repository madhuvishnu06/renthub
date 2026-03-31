// Chat functionality
document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messages-container")

  if (messagesContainer) {
    // Auto-scroll to bottom
    function scrollToBottom() {
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    }

    scrollToBottom()

    // Handle message form submission
    const messageForm = document.querySelector("form")
    const messageInput = document.getElementById("message-input")

    if (messageForm && messageInput) {
      messageForm.addEventListener("submit", () => {
        setTimeout(scrollToBottom, 100)
      })

      // Enter to send (Shift+Enter for new line)
      messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault()
          messageForm.submit()
        }
      })
    }

    // Simple polling for new messages (every 5 seconds)
    // In production, use WebSockets for real-time updates
    const currentUrl = window.location.href
    if (currentUrl.includes("/chat/") && !currentUrl.includes("/delete/")) {
      setInterval(() => {
        // This is a placeholder for real-time functionality
        // In a real app, you'd use AJAX to fetch new messages
        console.log("[Chat] Checking for new messages...")
      }, 5000)
    }
  }
})
