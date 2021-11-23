let currentPage = 1

let pageLimit = 10


const getPage = (e) => {
    e.preventDefault()

    if (e.target.innerText === '»') {
        currentPage += 1
    }
    else if (e.target.innerText === '«') {
        if (currentPage > 1) currentPage -= 1
    }
    else {
        currentPage = parseInt(e.target.innerText)
    }

    console.log(`/account/orders`)
    console.log(`/account/orders?page=${currentPage}`)
    console.log(`/account/orders?page=${currentPage}&limit=${pageLimit}`)

    $.get(`/account/orders?page=${currentPage}&limit=${pageLimit}`, (res) => {
        renderOrders(JSON.parse(res))

        generatePaginationButtons()
    })
}

const renderOrders = (orders) => {
    const orderList = $('#orderProducts')

    orderList.empty()

    for (const i in orders) {
        const order = JSON.parse(orders[i])

        const orderDate = new Date(order.placed_at)

        orderList.append(`
        <div class="card mb-4">
            <div class="card-header">
                <div class="container">
                    <div class="row">
                        <div class="col float-left"><small class="text-muted">ORDER PLACED</small></div>
                        <div class="col"><small class="text-muted">TOTAL</small></div>
                        <div class="col-8"><small class="text-muted float-end">Order #: <a href="/order/${order.id}" class="link-unstyled" style="text-decoration: underline;">${order.id}</a></small></div>
                    </div>
                    <div class="row">
                        <div class="col float-left"><small class="text-muted">${orderDate.toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'})}</small></div>
                        <div class="col"><small class="text-muted">\$${order.cost}</small></div>
                        <div class="col-8"></div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <h5 class="card-title pb-2">Order Products <span class="badge bg-secondary">Shipped</span></h5>
                
                <div class="container" id="orderProducts${i}">
                    
                </div>
            </div>
        </div>
        `)

        const orderProductsElement = $(`#orderProducts${i}`)

        for (const j in order.products) {
            const product = JSON.parse(order.products[j])

            orderProductsElement.append(`
            <div class="row pb-2">
                <div class="col-md-2 float-left">
                    <img src="${product.url}" class="img-fluid rounded-start" alt="...">
                </div>
                <div class="col-md-10">
                    <div class="container">
                        <div class="row"><div class="col float-left">${product.name} <span class="badge ${product.status === 'delivered' ? 'bg-success' : 'bg-secondary'}">${product.status === 'delivered' ? 'Delivered' : 'Shipped'}</span></div></div>
                        <div class="row"><div class="col float-left"><small class="text-muted">Vendor</small></div></div>
                    </div>
                </div>
            </div>
            `)
        }
    }
}

const generatePaginationButtons = () => {
    var buttonList = $('#paginationList')

    buttonList.empty()

    console.log('yo')

    buttonList.append(`
        <li class="page-item pagi ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        </li>`)

    buttonList.append(`<li id="testid" class="page-item pagi ${currentPage === 1 ? 'active' : ''}"><a class="page-link" href="#">${currentPage === 1 ? 1 : currentPage - 1}</a></li>`)
    buttonList.append(`<li class="page-item pagi ${currentPage > 1 ? 'active' : ''}"><a class="page-link" href="#">${currentPage === 1 ? currentPage + 1 : currentPage}</a></li>`)
    buttonList.append(`<li class="page-item pagi"><a class="page-link" href="#">${currentPage === 1 ? currentPage + 2 : currentPage + 1}</a></li>`)

    buttonList.append(`
        <li class="page-item pagi">
            <a class="page-link" href="#" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        </li>`)

    $('.pagi').click(getPage)
} 



$(document).ready(generatePaginationButtons)
