const addProductModal = document.querySelector('.modal')
const startAddProductBtn = document.getElementById('start-add-product')
const cancelAddProdBtn = document.getElementById('cancel-product')
const backdrop = document.getElementById('backdrop')
const submitProdBtn = document.getElementById('product-submit')
const homeButton = document.getElementById('home-button')
const prodTitle = document.getElementById('title')
const prodPrice = document.getElementById('price')
const prodDescription = document.getElementById('description')
const prodMedia = document.getElementById('media')
const prodSize = document.getElementById('size')


const products = []

const updateUI = () => {
  const emptyDisplay = document.getElementById('entry-text')
  if (products.length === 0) {
    emptyDisplay.style.display = 'block'
  } else {
    emptyDisplay.style.display = 'none'
  }
}

const clearUserInput = () => {
  const userInputs = document.querySelectorAll('input')
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
}

const renderNewProduct = (title, price, description, media, size) => {
  const listRoot = document.getElementById('product-list')
  const newProductElement = document.createElement('li')
  newIdeaElement.className = 'idea-element'
  newIdeaElement.innerHTML = `
    <div class="idea-element__image"></div>
    <div class="idea-element__info">
      <h2>${title}</h2>
        <p>$${price}</p>
        <p>$${description}</p>
        <p>${media}</p>
        <p>${size}</p>
    </div>`

  // newIdeaElement.addEventListener('click', startDeleteProdHandler)
  listRoot.appendChild(newProductElement)
}

const submitProductHandler = () => {
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
  renderNewProduct()
  console.log(products)
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
homeButton.addEventListener('click', () => {
  window.location.href = '/'
})
