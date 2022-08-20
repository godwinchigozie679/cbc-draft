
$(document).ready(function(){

  $('.tutor-clear-all-filter').hide();  
  $('#ajaxLoader').hide();
  $('.filter-course-page').on('click', function(){    
    var _filterObj = {};
    $('.filter-course-page').each(function(index, ele){      
      var _filterVal = $(this).val();
      var _filterKey = $(this).data('filter');
      _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el) {
        return el.value;
      })
      // console.log(_filterObj);
    });
    
    // AJAX
    $.ajax(
      {
        url: '/course-page-filter',
        // method: 'post',
        data:_filterObj,
        dataType: 'json',
        beforeSend: function() {
          $('#ajaxLoader').show();

        },
        success:function(res){
          console.log(res);
          $('#course-page-filter-data').html(res.courses);
          $('#ajaxLoader').hide();         
          $('.tutor-clear-all-filter').show();
          
        }

      }
    )
  })


})



// Uncheck

$(document).ready(function(){  

  $('#ajaxLoader').hide();
    // Unchecked and Cancel Filter
      $(".uncheck").click(function(){
        $(".filter-course-page").prop("checked", false);
        var _filterObj = {};
        var _filterVal = $(this).val();
          var _filterKey = $(this).data('filter');
          _filterObj[_filterKey] = Array.from(document.querySelectorAll('div[data-filter='+_filterKey+']')).map(function(el) {
            return el.value;
          })
          // console.log(_filterObj);


          // Ajax
          $.ajax(
            {
              url: '/course-page-filter',
              // method: 'post',
              data:_filterObj,
              dataType: 'json',
              beforeSend: function() {
                $('#ajaxLoader').show();
      
              },
              success:function(res){
                $('.tutor-clear-all-filter').hide();                
                console.log(res);
                $('#course-page-filter-data').html(res.courses);
                $('#ajaxLoader').hide();
                
              }
      
            }
          )

    });
 
})




