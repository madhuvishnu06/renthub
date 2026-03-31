// Mobile Navigation Toggle
document.addEventListener("DOMContentLoaded", () => {
  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(".alert")
  messages.forEach((message) => {
    setTimeout(() => {
      message.style.transition = "opacity 0.5s"
      message.style.opacity = "0"
      setTimeout(() => message.remove(), 500)
    }, 5000)
  })

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
})

// Form validation helper
function validateForm(formId) {
  const form = document.getElementById(formId)
  if (!form) return true

  const inputs = form.querySelectorAll("input[required], select[required], textarea[required]")
  let isValid = true

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      isValid = false
      input.style.borderColor = "var(--color-error)"
    } else {
      input.style.borderColor = "var(--color-border)"
    }
  })

  return isValid
}

// Price calculation helper (will be used for booking)
function calculateRentalPrice(dailyRate, startDate, endDate) {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24))
  return days * dailyRate
}

// Image preview for file uploads
function previewImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const preview = document.getElementById("image-preview")
      if (preview) {
        preview.src = e.target.result
        preview.style.display = "block"
      }
    }
    reader.readAsDataURL(input.files[0])
  }
}
