const stripe = Stripe("pk_live_51HX7VpGoBx998m4u1vDJjCNCUvk66y51WuXRNLOO76sFwT2oPNo0PiLRit103LfyUHcVuRBdwN9OjW9vUiYXDphG00DS8qetWJ")
const checkoutBtn = document.getElementById('checkout-button')
const clearCartBtn = document.getElementById('remove-all-items')

clearCartBtn.addEventListener('click', () => {
  console.log('Clicked')
  window.location.href = "/cart/clear-cart"
})

checkoutBtn.addEventListener('click', () => {
  fetch('/create_session', {
    method: 'POST',
  })
  .then(function (response) {
    console.log(response)
    return response.json()
  })
  .then(function (session) {
    console.log(session)
    return stripe.redirectToCheckout({ sessionId: session.id })
  })
  .then (function (result) {
    if (result.error) {
      alert(result.error.message)
    }
  })
  .catch(function (error) {
    console.error({'Error': error})
  })
})
