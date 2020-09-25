const logInSwitch = document.getElementById('log-in-switch')
const signUpSwitch = document.getElementById('sign-up-switch')
const signUpForm = document.querySelector('.sign-up')
const logInForm = document.querySelector('.log-in')

logInSwitch.addEventListener('click', () => {
  logInForm.style.display = 'none'
  signUpForm.style.display = 'block'
})

signUpSwitch.addEventListener('click', () => {
  signUpForm.style.display = 'none'
  logInForm.style.display = 'block'
})
