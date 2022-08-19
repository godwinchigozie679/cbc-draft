const url_ = window.location.href //Grap the Url
const get_slug = window.location.href.split('/') //Grap the Url
var main_slug = get_slug.pop() || get_slug.pop();
// console.log(main_slug, '.....')


$(document).ready(function(){

  $('.tutor-clear-all-filter').hide();  
  $('#ajaxLoader').hide();
  $('.filter-course-category').on('click', function(){    
    var _filterObj = {'slug':[main_slug]};
    $('.filter-course-category').each(function(index, ele){      
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
        
        url: `/category-filter`,
        // method: 'post',        
        data:_filterObj,
        dataType: 'json',
        beforeSend: function() {          
          $('#ajaxLoader').show();          
        },
        success:function(res){
          console.log(_filterObj);
          console.log(url_);
          console.log(res);
          $('#course-category-filter-data').html(res.courses);
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
        $(".filter-course-category").prop("checked", false);
        var _filterObj = {'slug':[main_slug]};
        var _filterVal = $(this).val();
          var _filterKey = $(this).data('filter');
          _filterObj[_filterKey] = Array.from(document.querySelectorAll('div[data-filter='+_filterKey+']')).map(function(el) {
            return el.value;
          })
          // console.log(_filterObj);


          // Ajax
          $.ajax(
            {
              url: `/category-filter`,
              // method: 'post',
              data:_filterObj,
              dataType: 'json',
              beforeSend: function() {
                $('#ajaxLoader').show();
      
              },
              success:function(res){
                $('.tutor-clear-all-filter').hide();                
                console.log(res);
                $('#course-category-filter-data').html(res.courses);
                $('#ajaxLoader').hide();
                
              }
      
            }
          )

    });
 
})




