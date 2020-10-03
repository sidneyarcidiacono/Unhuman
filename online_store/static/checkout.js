const stripe = Stripe("pk_test_51HX7VpGoBx998m4uTzM1HqKlMxzsmTznqYcinrOt5ZmMjny9i6WWE5cGlwSFRuioBBq32YRDgjOXD0nuEMGFcxUS00jEe5QOaz")
const checkoutBtn = document.getElementById('checkout-button')
const clearCartBtn = document.getElementById('remove-all-items')

clearCartBtn.addEventListener('click', () => {
  console.log('Clicked')
  window.location.href = '/clear-cart'
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
