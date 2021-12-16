function postForm(path, params, method) {
    method = method || 'post';

    var form = document.createElement('form');
    form.setAttribute('method', method);
    form.setAttribute('action', path);

    for (var key in params) {
        if (params.hasOwnProperty(key)) {
            var hiddenField = document.createElement('input');
            hiddenField.setAttribute('type', 'hidden');
            hiddenField.setAttribute('name', key);
            hiddenField.setAttribute('value', params[key]);
            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


function pay_by_ecpay(data) {
    json_data = JSON.stringify(data)
    url = 'http://192.168.5.181:5000/payment/to_ecpay'
    payment_page = 'http://192.168.5.181:5000/payment/payment_page'

    fetch(url, {
        method : "POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: json_data,
        })
        .then(res => res.json())
        .then(data => obj = data)
        .then(() => {
            console.log('OK')
            postForm(payment_page, {"html": obj.page})
        })        
    }


function sorted_by_price() {
    search_by_price = ""
    fetch(url, {
        method : "POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: json_data,
        })
        .then(res => res.json())
        .then(data => obj = data)
        .then(() => {
            console.log('OK')
        })        
}
