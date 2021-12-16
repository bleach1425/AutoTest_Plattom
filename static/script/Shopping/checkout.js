var num = 0

function fix() {
    num += 1
    if (num % 2 == 1) {
        document.getElementById("switch").textContent = "自訂資料"
        $("input").removeAttr("readonly")
        // })
    } else {
        document.getElementById("switch").textContent = "預設資料"
        $("input").attr("readonly", true)
    }
}
