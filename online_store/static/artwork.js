const productImages = document.querySelectorAll('#product-image')
const seeMoreButtons = document.querySelectorAll('.see-more-icon')
const cancelAddBtn = document.getElementById('cancel-add-icon')
// const backdrop = document.getElementById('backdrop')
const gallery = document.querySelector('.gallery')

// const toggleBackdropHandler = () => {
//   backdrop.classList.toggle('visible')
// }

const showProductModalHandler = productId => {
  const productModal = document.getElementById(productId)
  // toggleBackdropHandler()
  gallery.classList.toggle('invisible')
  productModal.classList.add('visible')
}

const closeProductModal = productId => {
  const productModal = document.getElementById(productId)
  gallery.classList.toggle('invisible')
  productModal.classList.remove('visible')
  // toggleBackdropHandler()
}

const backdropClickHandler = () => {
  closeProductModal()
  // toggleBackdropHandler()
}

// window.addEventListener('click', () => {
//   if (backdrop.classList.contains('visible')) {
//     backdropClickHandler
//   }
// })
