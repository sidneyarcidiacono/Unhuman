// TODO: Clean up scope of variables

const addProductModal = document.querySelector('.modal')
const startAddProductBtn = document.getElementById('start-add-product')
const cancelAddProdBtn = document.getElementById('cancel-product')
const backdrop = document.getElementById('backdrop')
const submitProdBtn = document.getElementById('product-submit')
const removeProductBtn = document.getElementById('remove-button')
const homeButton = document.getElementById('home-button')
const prodTitle = document.getElementById('title')
const prodPrice = document.getElementById('price')
const prodDescription = document.getElementById('description')
const prodMedia = document.getElementById('media')
const prodSize = document.getElementById('size')
const productManager = document.querySelector('.product-manager')

products = []

const clearUserInput = () => {
  const userInputs = document.querySelectorAll('input')
  console.log(products)
  for (const input of userInputs) {
    if (input !== prodPrice) {
      input.value = ''
    } else {
      input.value = 0
    }
  }
}

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

const submitProductHandler = () => {
  const title = prodTitle.value
  const price = prodPrice.value
  const description = prodDescription.value
  const media = prodMedia.value
  const size = prodSize.value

  const newProduct = {
    title: title,
    price: price,
    description: description,
    media: media,
    size: size
  }
  // products.push(newProduct)
  // console.log(`Products: ${products}`)
}

const prodCancelBtnHandler = () => {
  closeProdForm()
}

const backdropClickHandler = () => {
  closeProdForm()
  clearUserInput()
}

startAddProductBtn.addEventListener('click', showAddProdForm)
submitProdBtn.addEventListener('click', submitProductHandler)
cancelAddProdBtn.addEventListener('click', prodCancelBtnHandler)
backdrop.addEventListener('click', backdropClickHandler)
// homeButton.addEventListener('click', () => {
//   window.location.href = '/'
// })
