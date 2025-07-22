// ///////////////// navbar underline
const links1 = document.querySelectorAll('.underline ul li a');
const menuBtn1 = document.querySelector("#menu-btn")
const menu1 = document.querySelector(".underline .main-nav .nav-container")
const currentPage = window.location.pathname;

links1.forEach((link) => {
  link.classList.remove("active");
});

links1.forEach((link) => {
  if (link.getAttribute("href") === currentPage) {
    link.classList.add("active");
  }
});
// links1.forEach((link) => {
//   link.addEventListener("click", () => {
//     links1.forEach((link) => {
//       link.classList.remove("active")
//     })
//     link.classList.add("active")
//     if (window.innerWidth < 991) {
//       menu1.classList.toggle("right")
//       menuBtn1.classList.toggle("closeMenu")
//     }
//   })
// })

menuBtn1?.addEventListener("click", () => {
  menuBtn1.classList.toggle("closeMenu")
  menu1.classList.toggle("right")
})

// popup
const popup = document.querySelector(".underline .main-nav .nav-container .popup")
console.log(popup)
popup?.addEventListener("click", () => {
  menu1.classList.remove("right")
  menuBtn1.classList.toggle("closeMenu")
})


// For Language




const authEmailInput = document.querySelector('#auth-form #email')
const authPasswordInput = document.querySelector('#auth-form #password')
const authAcceptTermsInput = document.querySelector('#auth-form #accept-terms')
const authNameInput = document.querySelector('#auth-form #name')
const authRePasswordInput = document.querySelector('#auth-form #rePassword')
const authMobileInput = document.querySelector('#auth-form #mobile')
const authBirthdayInput = document.querySelector('#auth-form #birthday')
const authGenderInput = document.querySelector('#auth-form #gender')


if (authGenderInput) {
  authGenderInput.addEventListener('input', function (e) {
    if (e.target.value) {
      authGenderInput.classList.add('has-value');
      const parentElement = authGenderInput.closest('.input-container');

      parentElement.classList.remove('has-error')
      parentElement.querySelector('.err-msg').textContent = ""
    } else {
      authGenderInput.classList.remove('has-value');
    }
  })
}

let allInputs = document.querySelectorAll('input');


allInputs.forEach(input => {
  input.addEventListener('input', function (e) {
    if (e.target.value) {
      input.classList.add('has-value');
      const parentElement = input.closest('.input-container');


      parentElement.classList.remove('has-error')
      parentElement.querySelector('.err-msg').textContent = ""
    } else {
      input.classList.remove('has-value');
    }
  })
})

authAcceptTermsInput && authAcceptTermsInput.addEventListener('click', () => {
  if (authAcceptTermsInput.checked) {
    const parentElement = authAcceptTermsInput.closest('.input-container');
    parentElement.classList.remove('has-error')
    parentElement.querySelector('.err-msg').textContent = ""
  }
})

const passwordIcons = document.querySelectorAll('.input-password .password-icon');

passwordIcons.forEach(icon => {
  icon.addEventListener("click", () => {
    if (icon.parentNode.children[0].type === "password") {
      icon.parentNode.children[0].type = "text";
      console.log('iconiconiconicon text', icon.parentNode.children[0])

      icon.parentNode.children[2].querySelector('img').src = "/assets/run2mind/images/show-show.svg"
    } else {
      icon.parentNode.children[0].type = "password";
      icon.parentNode.children[2].querySelector('img').src = "/assets/run2mind/images/hide.svg"
      // console.log('iconiconiconicon password', icon.parentNode.children[2].querySelector('img'))

    }
  })
})





const authBtn = document.querySelector('#auth-btn')

/*
authBtn.onclick = function handleAuthSubmit(e) {
  e.preventDefault();


  const parentEmailElement = authEmailInput?.closest('.input-container');
  const parentPasswordElement = authPasswordInput?.closest('.input-container');
  const parentAcceptTermsElement = authAcceptTermsInput?.closest('.input-container');
  const parentNameElement = authNameInput?.closest('.input-container');
  const parentRePasswordElement = authRePasswordInput?.closest('.input-container');
  const parentMobileElement = authMobileInput?.closest('.input-container');
  const parentBirthdayElement = authBirthdayInput?.closest('.input-container');
  const parentGenderElement = authGenderInput?.closest('.input-container');

  if (!authEmailInput.value) {
    parentEmailElement.classList.add('has-error')
    parentEmailElement.querySelector('.err-msg').textContent = "Please enter your mail!!"
  }

  if (!authPasswordInput.value) {
    parentPasswordElement.classList.add('has-error')
    parentPasswordElement.querySelector('.err-msg').textContent = "Please enter your password"
  }


  if (!authAcceptTermsInput.checked) {
    parentAcceptTermsElement.classList.add('has-error')
    parentAcceptTermsElement.querySelector('.err-msg').textContent = "Please enter your password"
  }

  if (!authNameInput.value) {
    parentNameElement.classList.add('has-error')
    parentNameElement.querySelector('.err-msg').textContent = "Please writing your nick name"
  }


  if (!authRePasswordInput.value) {
    parentRePasswordElement.classList.add('has-error')
    parentRePasswordElement.querySelector('.err-msg').textContent = "Please enter your password"
  }

  if (!authMobileInput.value) {
    parentMobileElement.classList.add('has-error')
    parentMobileElement.querySelector('.err-msg').textContent = "Please enter your mobile"
  }

  if (!authBirthdayInput.value) {
    parentBirthdayElement.classList.add('has-error')
    parentBirthdayElement.querySelector('.err-msg').textContent = "Please enter your birthday"
  }

  if (!authGenderInput.value) {
    parentGenderElement.classList.add('has-error')
    parentGenderElement.querySelector('.err-msg').textContent = "Please enter your birthday"
  }


}
*/
