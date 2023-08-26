let updateBtn = document.getElementsByClassName('update-cart')

for(let i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('Product id:', productId, 'Action:', action)

        console.log('User:', user)
        if(user === 'AnonymousUser') {
            console.log('Not logged in!')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User logged in.')

    let url = '/update_item/'

    // fetch(url, {
    //     method: "POST",
    //     headers: {
    //         'Content-Type':'application/json',
    //         'X-CSRFToken': csrftoken
    //     },
    //     body: JSON.stringify({'productId': productId, 'action': action})
    // })
    // .then((response) => {
    //     return response.json()
    // })
    // .then((data) => {
    //     console.log('data:', data)
    // })

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload()
    })
    .catch((error) => {
        console.log('There was a problem with the fetch operation:', error.message);
    });
}

