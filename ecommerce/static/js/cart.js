let updateBtn = document.getElementsByClassName('update-cart')

for(let i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('Product id:', productId, 'Action:', action)

        console.log('User:', user)
        if(user == 'AnonymousUser') {
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in..!')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity' : 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove item')
            delete cart[productId]
        }
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

async function updateUserOrder(productId, action) {
    console.log('User logged in.');

    const url = '/update_item/';

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('data:', data);

        // Reload the page to reflect changes
        location.reload();
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error.message);
    }
}

