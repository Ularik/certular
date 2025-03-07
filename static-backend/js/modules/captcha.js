window.onloadTurnstileCallback = function () {
  turnstile.render("#myWidget", {
    sitekey: "0x4AAAAAAA_zZk8YrdxHSfsQ",
    callback: function (token) {
      console.log(`Challenge Success ${token}`);
      setTimeout(() => {
        document.querySelector('.content-wrapper').style.display = 'block';
        document.querySelector('.captcha-modal-window').style.display = 'none';
      }, 2000)
    },
  });
};