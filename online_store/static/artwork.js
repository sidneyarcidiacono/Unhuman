const productImages = document.querySelectorAll('#product-image')
const seeMoreButtons = document.querySelectorAll('.see-more-icon')
const cancelAddBtn = document.getElementById('cancel-add-icon')
// const backdrop = document.getElementById('backdrop')
const gallery = document.querySelector('.gallery')
const galleryItems = document.querySelectorAll('.gallery-item')
const filter = document.getElementById('media')

const filterGallery = () => {
  for (galleryItem of galleryItems) {
    const itemMedia = galleryItem.dataset.media
    if (filter.value == 'Paintings') {
      if (itemMedia != 'Oil on Canvas') {
        galleryItem.classList.add('invisible')
      } else {
        galleryItem.classList.remove('invisible')
      }
    } else if (filter.value == 'Prints') {
      if (itemMedia != 'Print') {
        galleryItem.classList.add('invisible')
      } else {
        galleryItem.classList.remove('invisible')
      }
    } else if (filter.value == 'Full Gallery' && galleryItem.classList.contains('invisible')) {
      galleryItem.classList.remove('invisible')
    }
  }
}

const showProductModalHandler = productId => {
  const productModal = document.getElementById(productId)
  // toggleBackdropHandler()
  filter.classList.toggle('invisible')
  gallery.classList.toggle('invisible')
  productModal.classList.add('visible')
}

const closeProductModal = productId => {
  const productModal = document.getElementById(productId)
  gallery.classList.toggle('invisible')
  filter.classList.toggle('invisible')
  productModal.classList.remove('visible')
  // toggleBackdropHandler()
}

const backdropClickHandler = () => {
  closeProductModal()
  // toggleBackdropHandler()
}

filter.addEventListener('change', filterGallery)
