function All_Things_I_Should_do() {
  document.body.innerHTML +=
    '<button id="settingsBtn" class="toggle-btn">\
        <div class="icooon"></div>\
      </button>\
      <div id="fly">\
      <!-- 右侧滑入菜单 -->\
      <div id="rightMenu" class="menu hidden">\
      <div class="my_card">\
          <h2>核能运动会操作系统</h2>\
      </div>\
      </div>\
    </div>\
    <div id="chat-container"></div><ul class="background">\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
    <li></li>\
  </ul>\
  <div class="message"></div>';
  document.head.innerHTML +=
    '<link rel="stylesheet" type="text/css" href="managerMenu.css" />\
    <meta charset="UTF-8" />\
    <title>核能运动会操作系统</title>';
  let rightMenu = document.getElementById("rightMenu");
  fetch("/api/manager_page")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(rightMenu);
      data.forEach((item) => {
        const name = item.Name;
        const address = item.Address;
        console.log(`Name: ${name}, Address: ${address}`);

        // 创建一个新的button元素，并设置其name和href属性
        const newButton = document.createElement("a");
        newButton.textContent = name;
        newButton.setAttribute("href", address);
        newButton.className = "To";

        // 将新创建的button元素添加到页面中
        rightMenu.appendChild(newButton);
        rightMenu.innerHTML+="<br>"
      });
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });

  /* Play an animation on each click */
  let btn = document.getElementById("settingsBtn");
  let MenuIcon = document.getElementsByClassName("icooon")[0];
  let menuForward = bodymovin.loadAnimation({
    container: MenuIcon,
    renderer: "svg",
    loop: false,
    autoplay: false,
    path: "menuV2.json",
  });
  var directionMenu = 1;
  btn.addEventListener("click", function () {
    menuForward.setDirection(directionMenu);
    menuForward.play();
    directionMenu = -directionMenu;
    var fly = document.getElementById("fly");
    fly.classList.toggle("hidden");
    if (!fly.classList.contains("hidden")) {
      fly.style.right = "-340px";
    } else {
      fly.style.right = "10px";
    }
  });
}
function showMessage(message) {
  var msgElement = document.querySelector(".message");
  msgElement.innerHTML = message;
  msgElement.style.display = "block";
  msgElement.style["background-color"] = "#f8f8f8";

  setTimeout(function () {
    msgElement.style.display = "none";
  }, 3000);
}
function warningMessage(message) {
  var msgElement = document.querySelector(".message");
  msgElement.innerHTML = message;
  msgElement.style.display = "block";
  msgElement.style["background-color"] = "#ffef5c";

  setTimeout(function () {
    msgElement.style.display = "none";
  }, 3000);
}

function errorMessage(message) {
  var msgElement = document.querySelector(".message");
  msgElement.innerHTML = message;
  msgElement.style.display = "block";
  msgElement.style["background-color"] = "#ec261b";

  setTimeout(function () {
    msgElement.style.display = "none";
  }, 3000);
}
