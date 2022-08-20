//SCROLL TOP FUCNTION
const scrollShowShare  = document.getElementById('show-share');
const scrollCloseShare = document.getElementById('close-share');
const socialVar = document.getElementById('social-share')
console.log(socialVar)
// Show
scrollShowShare.addEventListener('click', scrollUpShowShare);
// Show
scrollCloseShare.addEventListener('click', scrollUpCloseShare);

// When the user scrolls down 20px from the top of the document, show the button
// for scrolling down
window.onscroll = function scrollUpShowShare() {
  if (window.pageYOffset > 400 || document.documentElement.scrollTop > 400 || document.body.scrollTop > 400) {
    scrollShowShare.classList.remove('d-none');
    // close
    scrollCloseShare.classList.remove('d-block');
    scrollCloseShare.classList.add('d-none');
    // Social Content
    socialVar.classList.remove('d-block')
    socialVar.classList.add('d-none')
    
  } else {
    scrollShowShare.classList.add('d-block');
    scrollShowShare.classList.remove('d-block');
    scrollShowShare.classList.add('d-none');
    
  }
  
};


// Show
function scrollUpShowShare(){
  
  socialVar.classList.remove('d-none');
  socialVar.classList.add('d-block');
  scrollShowShare.classList.add('d-none');
  scrollCloseShare.classList.remove('d-none');
  scrollCloseShare.classList.add('d-block')  
}


// Close Social Share

function scrollUpCloseShare(){
    
  socialVar.classList.remove('d-block');
  socialVar.classList.add('d-none');  
  scrollCloseShare.classList.remove('d-block');
  scrollCloseShare.classList.add('d-none');
  scrollShowShare.classList.remove('d-none');
  scrollShowShare.classList.add('d-block');
  socialVar.classList.add('d-none');
};







