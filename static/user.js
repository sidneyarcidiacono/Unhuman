const logInSwitch = document.getElementById('log-in-switch')
const signUpSwitch = document.getElementById('sign-up-switch')
const signUpForm = document.querySelector('.sign-up')
const logInForm = document.querySelector('.log-in')

const toggleHelper = () => {
  logInForm.classList.remove('invisible')
}

const logInSwitchHandler = () => {
  logInForm.classList.toggle('invisible')
}

const signUpSwitchHandler = () => {
  signUpForm.classList.toggle('invisible')
  logInForm.classList.add('invisible')
}

window.addEventListener('load', toggleHelper)
logInSwitch.addEventListener('click', logInSwitchHandler)
signUpSwitch.addEventListener('click', signUpSwitchHandler)
