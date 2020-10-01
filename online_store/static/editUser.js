const editProfile = document.getElementById('edit-user')
const editForm = document.querySelector('form')
const editUserCancel = document.getElementById('edit-user-cancel')
const logOutButton = document.getElementById('log-out')

editProfile.addEventListener('click', () => {
  editForm.classList.remove('invisible')
})

editUserCancel.addEventListener('click', () => {
  editForm.classList.add('invisible')
})

logOutButton.addEventListener('click', () => {
  window.location.href = '/logout'
})
