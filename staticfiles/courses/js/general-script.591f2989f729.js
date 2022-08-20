
// FILTER DISPLAY
const courseGeneralFilterSM = document.getElementById('filter-course-sm');
const courseFilterColumn = document.getElementById('filter-column');
const closeFilter = document.getElementById('close-filter')

function myCourseFilter() {
    courseGeneralFilterSM.classList.remove('d-xl-none');
    courseGeneralFilterSM.classList.add('d-none')

    // Show filter
    courseFilterColumn.classList.remove('d-none');
    courseFilterColumn.classList.add('d-block');
    courseFilterColumn.classList.add('filter-column-style');

    // Show close Filter
    closeFilter.classList.remove('d-none');
    closeFilter.classList.add('d-block');
  }




  // CLose Filter Tab

  function myCloseFilter() {
    courseGeneralFilterSM.classList.remove('d-none');
    courseGeneralFilterSM.classList.add('d-xl-none')

    // Show filter
    courseFilterColumn.classList.remove('d-block');
    courseFilterColumn.classList.add('d-none');
    courseFilterColumn.classList.remove('filter-column-style');

    // Show close Filter
    closeFilter.classList.remove('d-block');
    closeFilter.classList.add('d-none');
  }