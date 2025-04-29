document.addEventListener("DOMContentLoaded", function () {
  // Toggle Sidebarのボタン
  document.querySelector("button").addEventListener("click", function () {
    var sidebar = document.getElementById("sidebar");
    if (sidebar.style.display === "none" || sidebar.style.display === "") {
      sidebar.style.display = "block"; // サイドバーを表示
    } else {
      sidebar.style.display = "none"; // サイドバーを非表示
    }
  });

  // 閉じるボタン
  document.getElementById("close-btn").addEventListener("click", function () {
    var sidebar = document.getElementById("sidebar");
    sidebar.style.display = "none"; // サイドバーを非表示にする
  });
});
