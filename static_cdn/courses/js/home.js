
$(document).ready(function(){
  $('#ajaxHomeLoader').hide();
  $('.filter-home-button').on('click', function(){
    var _filterObj = {};
    var _filterVal = $(this).val();
      var _filterKey = $(this).data('filter');
      _filterObj[_filterKey] = Array.from(document.querySelectorAll('button[data-filter='+_filterKey+']')).map(function(el) {
        return el.value;
      })
      console.log(_filterObj);
    // $('.filter-home-button').each(function(index, ele){
      

    // })

    $.ajax(
      {
        url: '/home-filter-data',
        // method: 'post',
        data:_filterObj,
        dataType: 'json',
        beforeSend: function() {
          $('#ajaxHomeLoader').show();

        },
        success:function(res){
          console.log(res);
          $('#home-filter-data').html(res.courses);
          $('#ajaxHomeLoader').hide();
        }

      }
    )


  })
})