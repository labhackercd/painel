loadContainers();
// Concatenação de filtros na URL e atualização de labels.
// var url foi setada antes do $.getJSON do worldcloud
var url = new URL(window.location.href);
var category_id = url.searchParams.get("category_id");
var title_date = localStorage.getItem("show_by");

$('.js-category').click(function (e) {
  var categoryId = $(e.target).data('categoryId');
  if (categoryId === 0) {
    localStorage.removeItem('category_id');
  }
  else {
    localStorage.setItem('category_id', categoryId);
  }
  loadContainers();
});

// pegar url atual, ver se tem parametros, se tiver add

$('.js-filter-buttons button').click(function() {
  if ($(this).hasClass('-day')) {
    localStorage.removeItem('show_by');
  } else if ($(this).hasClass('-week')) {
    localStorage.setItem('show_by', 'week')
  } else if ($(this).hasClass('-month')) {
    localStorage.setItem('show_by', 'month')
  }
  loadContainers();
});

var offset = parseInt(localStorage.getItem("offset"));

if (!offset || offset === 0) {
  $('.js-offset-next').addClass('-disabled');
}

$('.js-offset-next').click(function() {
  if (offset === 1) {
    localStorage.removeItem('offset');
    offset = 0;
  } else if (!offset || offset === 0) {
    return
  } else {
    localStorage.setItem('offset', offset - 1);
  }
  if (!localStorage.getItem("offset")) {
    $('.js-offset-next').addClass('-disabled');
  } else { 
    $('.js-offset-next').removeClass('-disabled');
    offset = parseInt(localStorage.getItem("offset"));
  }
  loadContainers();
})

$('.js-offset-prev').click(function() {
  if (offset) {
    localStorage.setItem('offset', offset + 1);
  } else {
    localStorage.setItem('offset', 1);
  }
  if (!localStorage.getItem("offset")) {
    $('.js-offset-next').addClass('-disabled');
  } else { 
    $('.js-offset-next').removeClass('-disabled');
    offset = parseInt(localStorage.getItem("offset"));
  }
  loadContainers();
})

function loadContainers() {
  loadChart();
  loadWordCloud();
  loadTopTweets();
  loadTopProfiles();
}