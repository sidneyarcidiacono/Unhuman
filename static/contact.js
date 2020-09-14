const homeButton = document.getElementById('homeButton')
const addProductModal = document.querySelector('.modal')
const startAddProductBtn = document.getElementById('start-add-product')
const cancelAddProdBtn = document.getElementById('cancel-product')
const backdrop = document.getElementById('backdrop')
const submitProdBtn = document.getElementById('product-submit')
const emptyDisplay = document.getElementById('entry-text')
const userInputs = document.querySelectorAll('input')
const prodTitle = document.getElementById('title')
const prodPrice = document.getElementById('price')
const prodDescription = document.getElementById('description')
const prodMedia = document.getElementById('media')
const prodSize = document.getElementById('size')

const products = []

const updateUI = () => {
  if (products.length === 0) {
    emptyDisplay.style.display = 'block'
  } else {
    emptyDisplay.style.display = 'none'
  }
}

const clearUserInput = () => {
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
}

const showAddProdForm = () => {
  addProductModal.classList.add('visible')
  toggleBackdropHandler()
}

const closeProdForm = () => {
  addProductModal.classList.remove('visible')
  toggleBackdropHandler()
  clearUserInput()
}

const startAddProductHandler = () => {
  const title = prodTitle.value
  const price = prodPrice.value
  const description = prodDescription.value
  const media = prodMedia.value
  const size = prodSize.value

  if (
    title.trim() === '' ||
    price.trim() === '' ||
    description.trim() === '' ||
    media.trim() === '' ||
    size.trim() === '' ||
    !title ||
    !price ||
    !description ||
    !media ||
    !size
  ) {
    alert('Please complete all fields.')
    return
  }
  const newProduct = {
    id: Math.random().toString(),
    title: title,
    price: price,
    description: description,
    media: media,
    size: size
  }
  products.push(newProduct)
  console.log(products)
}

const prodCancelBtnHandler = () => {
  closeProdForm()
}

startAddProductBtn.addEventListener('click', showAddProdForm)
cancelAddProdBtn.addEventListener('click', prodCancelBtnHandler)
homeButton.addEventListener('click', (e) => {
  window.location.href = '/'
})
