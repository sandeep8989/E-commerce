!function(e,t){"localStorage"in e&&localStorage.getItem("gmtNightMode")&&(t.documentElement.className+=" night-mode")}(window,document),function(e,t){var o;"localStorage"in e&&((o=t.querySelector("#night-mode"))&&o.addEventListener("click",function(e){e.preventDefault(),t.documentElement.classList.toggle("night-mode"),t.documentElement.classList.contains("night-mode")?localStorage.setItem("gmtNightMode",!0):localStorage.removeItem("gmtNightMode")},!1))}(window,document);