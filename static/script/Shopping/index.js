var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);


function add_to_carts(...items) {
    url = "http://192.168.5.181:5000/shopping/carts";
    num = document.getElementById(items[0] + '_' + 'number');
    if ((num.value == 0) | (num.value == null)) {
        Swal.fire({
            icon: 'error',
            title: '無法加入購物車...',
            text: '數量為0或數量為空',
          })
    }
    else {
        // Get commodity information
        var obj = {
            "name": items[0],
            "price": items[1],
            "num": num.value
        }
        // console.log(obj)
        json_data = JSON.stringify(obj)
        
        // Fetch commodity information
        fetch(url, {
            method : "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body:json_data,
            }).then((response)=> {
            return response.text();
        })

        // Tip User result
        Swal.fire(
            '感謝您!',
            '商品已新增至購物車!',
            'success'
        ).then(function() {
            location.reload();
        })
    }

}



function reflash_page() {
    location.reload();
}


function check() {
    console.log('1')
    var min = $("#min").val();
    var max = $("#max").val();
    if (min == null || max == null || min=="" || max =="") {
        alert("最低價 or 最高價不得為空 !!")
        window.location.href="#"
        return false;
    }
    else {
        if (min > max) {
            alert("最低價不得大於最高價 !!")
            window.location.href="#"
            return false;
        }
    }
}


function funcUrlDel(name) {
    var loca = window.location
    var baseUrl = loca.search.substr(1);
    var query = loca.search.substr(1);
    if (query.indexOf(name) > -1) {
        var obj = {}
        var arr =  query.split("&")
        for (var i =0; i < arr.length; i++) {
            arr[i] = arr[i].split("=")
            obj[arr[i][0]] = arr[i][1];
        };
        delete obj[name]
        var url = baseUrl + JSON.stringify(obj).replace(/[\{\}]/g, "").replace(/\:/g, "=").replace(/\,/g,"&")
    }
}




var main_url = location.href.split('?')[0]

function sorted(...args) {
    a = '';
    var price_param = ''
    let domain = (new URL(window.location.href))
    if (args.includes('sorted')) {
        // window.location.href = '?sorted_by=' + args[1] + '&sorted=' + args[2];
        a += '?sorted_by=' + args[1] + '&sorted=' + args[2];
    }
    else if (args.includes('sorted_and_price')) {
        if (domain.search.search('sorted_by') == 21) {
            return
        }
        else {
            var price_param = location.search
            console.log(price_param)
            a += price_param
            a += '&sorted_by=' + args[1] + '&sorted=' + args[2];
            window.location.href = main_url + a
        }
    }
    else if (args.includes('price')) {
        // window.location.href = '?min=' + args[1] + '&max=' + args[2];
        a += '?min=' + args[1] + '&max=' + args[2];
    }
    else {
        alert('參數錯誤')
        return false;
    }
    window.location.href = 'index' + a
}
