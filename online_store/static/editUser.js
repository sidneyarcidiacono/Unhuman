const editProfile = document.getElementById('edit-user')
const editForm = document.querySelector('form')
const logOutButton = document.getElementById('log-out')

editProfile.addEventListener('click', () => {
  editForm.classList.toggle('invisible')
})

logOutButton.addEventListener('click', () => {
  window.location.href = '/logout'
})
