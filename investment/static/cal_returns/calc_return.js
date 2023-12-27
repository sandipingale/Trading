// To sarch the symbols
$(document).ready(function() {
    $('#id_symbol_name').select2({
        ajax: {
            url: "get_share_list",
            dataType: 'json',
            delay: 250,
            data: function (params) {
            return {
                q: params.term, // search term
                page: params.page
            };
            },
            processResults: function (data, params) {
            return {
                results: data.results,
                pagination: {
                more: (params.page * 30) < data.total_count
                }
            };
            },
            cache: true,
            minimumInputLength: 2,
        },
        minimumInputLength: 2,
    });
});
    
// Draw the apex chart    
function draw_chart(price_list, price1_list,date_list)
{
    var options = {
        chart: {
            type: 'line'
        },
        series: [{
            name: 'Investment',
            data: price_list
        },
        {
            name: 'Returns',
            data: price1_list
        }],
        xaxis: {
            categories: date_list,
            type: 'datetime',

        },
        yaxis:{
            tickAmount:6,
            labels: {
            formatter: (value) =>{
                if (value >= 100000)
                {
                return (value/100000).toFixed(2) + " Lac"
                }
                if (value > 1000)
                {
                return (value/1000).toFixed(2) + " K"
                }
                return value;
            }
            }
        },
        noData: {
            text: 'Loading...'
        },
        stroke:{
            width:1.5
        },
        tooltip:{
            x:{
            format: "dd MMM yyyy"
            }
        }
    }

    var chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
    chart.updateSeries([{
          name: 'Investment',
          data: price_list
        },
        {
          name: 'Returns',
          data: price1_list
        }])
    }
 
//Update the dates in input fields
document.getElementById("id_start_date").value = "2019-01-01";
document.getElementById("id_end_date").value = new Date().toISOString().substr(0, 10);

//Main method triggered on submit
function get_page_data(){
    document.getElementById("inv-test-result").style.opacity='0';
    e = document.getElementById("id_symbol_name");
    var text = e.options[e.selectedIndex].text;
    if (text.includes('---------------')){
        show_error_notification("Please select the symbol")
        return
    }
    start_date = document.getElementById("id_start_date").value;
    end_date = document.getElementById("id_end_date").value;
    risk_category = document.getElementById("id_risk_category").value;
    const csrftoken = getCookie('csrftoken');
    button = document.getElementById("id-submit");
    button.classList.add("is-loading");
    user = {
        "symbol": text,
        "start_date": start_date,
        "end_date": end_date,
        "category":risk_category,
        "age": "23"
    }

    let options = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(user)
    }
    fetch("get_inv_json",options)           //api for the get request
    .then(response => response.json())
    .then(data => {
        update_dom_with_data(data);
    });
    
}

//Function to create the table
function create_table(data)
{
    tbody = document.getElementById("id-table-body");
    while (tbody.hasChildNodes()) {
        tbody.removeChild(tbody.lastChild);
    }
    data.forEach((x,i)=>{
        trow = tbody.insertRow();
        tcell = trow.insertCell(0);
        tcell.innerHTML = x[0]
        tcell1 = trow.insertCell(1);
        tcell1.innerHTML = x[3].toFixed(2);
    })
}

//MEthod to update the dom elements
function update_dom_with_data(data)
{
    const f_list = ["symbol", "xirr", "inv_value", "total_ret", "total_inv", "inv_to_proceed", "abs_return"]
    f_list.forEach((x,i) => {
        dataElements = document.getElementsByClassName("class-" + x);

        for (let i = 0; i < dataElements.length; i++) 
        {
            if (x == 'abs_return')
            {
                dataElements[i].innerHTML = data[x] + "%";
            }
            else
            {
                dataElements[i].innerHTML = data[x];
            }
        
            if (x== 'xirr' || x== 'total_ret' || x == 'abs_return')
            {
                dataElements[i].classList.remove("has-text-danger", "has-text-success");
                if (data["abs_return"] < 0)
                {
                    dataElements[i].classList.add("has-text-danger");
                }
                else
                {
                    dataElements[i].classList.add("has-text-success");
                }
            }

        }

    })

    msg = document.getElementById("id-message");
    msg.classList.remove("has-text-danger", "has-text-success");
    msg.innerHTML = data['msg'];
    if (data['abs_return'] < 0)
    {
        msg.classList.add("has-text-danger")
    }
    else
    {
        msg.classList.add("has-text-success")
    }
    draw_chart(data['price_list'], data['price1_list'], data['date_list'])

    if ( $.fn.dataTable.isDataTable( '#example' ) ) 
    {
        table = $('#example').DataTable();
        table.destroy();
    }
    create_table(data['data']);
    table = $('#example').DataTable( {
        dom: 'Blfrtip',
        buttons: [
            'copy' , 'csv', 'excel', 'pdf', 'print'
        ]
    });
    
    button = document.getElementById("id-submit");
    button.classList.remove("is-loading");
    document.getElementById("inv-test-result").classList.remove("is-hidden");
    document.getElementById("inv-test-result").style.opacity='1';
}
    
//Method to get the csrf_token
function getCookie(name) 
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
   
//Show the error notifications
function show_error_notification(message)
{
    error_node = document.getElementById("error-notification");
    notification =document.createElement("div");
    notification.classList.add("notification", "is-danger", "is-light", "has-text-centered");
    delete_btn = document.createElement("button")
    delete_btn.classList.add("delete")
    notification.innerHTML = message
    notification.appendChild(delete_btn);
    error_node.style.opacity = '1';
    error_node.appendChild(notification);
    delete_btn.addEventListener('click', () => {
        error_node.removeChild(notification);
    })
}


    
    