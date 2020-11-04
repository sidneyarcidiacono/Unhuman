const addProductModal = document.querySelector('.modal')
const startAddProductBtn = document.getElementById('start-add-product')
const startEditProductBtn = document.getElementById('start-edit-product')
const cancelAddProdBtn = document.getElementById('cancel-product')
const backdrop = document.getElementById('backdrop')
const removeProductBtn = document.getElementById('remove-button')
const homeButton = document.getElementById('home-button')
const productManager = document.querySelector('.product-manager')

const toggleBackdropHandler = () => {
  backdrop.classList.toggle('visible')
  productManager.classList.toggle('invisible')
}

const showAddProdForm = () => {
  addProductModal.classList.add('visible')
  toggleBackdropHandler()
}

const closeProdForm = () => {
  addProductModal.classList.remove('visible')
  toggleBackdropHandler()
}

const prodCancelBtnHandler = () => {
  closeProdForm()
}

const backdropClickHandler = () => {
  closeProdForm()
}

startAddProductBtn.addEventListener('click', showAddProdForm)
startEditProductBtn.addEventListener('click', showEditProdForm)
cancelAddProdBtn.addEventListener('click', prodCancelBtnHandler)
backdrop.addEventListener('click', backdropClickHandler)
