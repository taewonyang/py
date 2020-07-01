  function request_btn() {
    name = $('#name_input').val()
    address = $('#address_input').val()
    memo = $('#memo_input').val()
    food_kind = $('#food_kind').val()

    if (name == ''){
      alert('상호명은??')
      $('#name_input').focus()
      return
    } else if (address == ''){
      alert('도로명주소 뭐야?')
      $('#address_input').focus()
      return
    }
    $.ajax({
      type: "POST",
      url: "/mylist", 
      data: {name_give:name, address_give:address, food_kind_give:food_kind, visit_give:$('input[name="visit_record"]:checked').val() , memo_give:memo},
      success: function(response){
        if(response['result']=="success" ) {
          alert("등록완료!") ;
        } else {
          alert('서버 오류!')
          window.location.reload();
        }
      }
    })

  } 
// $(document).ready(function() {
//   $('#list_box').html(''); 
//   listing();  
// })

// function listing() {
//   $.ajax({
//     type: "GET",
//     url: "/search", 
//     data: { },
//     success: function(response){
//       rows = response['store']

//       for (i=0; i<rows.length; i++) {
//         server_name = rows[i]['name']
//         server_address = rows[i]['address']
//         server_visit = rows[i]['visit']
//         server_memo = rows[i]['memo']

//         table_plus = "<tr>\
//         <td>"+server_name+"</td>\
//         <td>"+server_address+"</td>\
//         <td>"+server_visit+"</td>\
//         <td>"+server_memo+"</td>\
//         </tr>"
//         $('#list_box').append(table_plus)
//       }
//     }
//   })

// }