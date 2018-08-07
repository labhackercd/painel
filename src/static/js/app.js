function showLoader(loaderId) {
  $('#' + loaderId).addClass('-show');
}

function hideLoader(loaderId) {
  $('#' + loaderId).removeClass('-show');
}

// Concatenação de filtros na URL e atualização de labels.
// var url foi setada antes do $.getJSON do worldcloud
var category_id = url.searchParams.get("category_id");
var title_date = url.searchParams.get("show_by");

$('.js-category').click(function (e) {
  var categoryId = $(e.target).data('categoryId');
  if (categoryId === 0) {
    url.searchParams.delete('category_id');
  }
  else {
    url.searchParams.set('category_id', categoryId);
  }
  window.location = url;
});

// pegar url atual, ver se tem parametros, se tiver add

$('.js-filter-buttons button').click(function() {
  if ($(this).hasClass('-day')) {
    url.searchParams.delete('show_by')
  } else if ($(this).hasClass('-week')) {
    url.searchParams.set('show_by', 'week')
  } else if ($(this).hasClass('-month')) {
    url.searchParams.set('show_by', 'month')
  }
  window.location = url;
});

var offset = parseInt(url.searchParams.get('offset'));

if (!offset || offset === 0) {
  $('.js-offset-next').addClass('-disabled');
} else {
  $('.js-offset-next').click(function() {
    if (offset === 1) {
      url.searchParams.delete('offset');
    } else {
      url.searchParams.set('offset', offset - 1);
    }

    window.location = url;
  })
}

$('.js-offset-prev').click(function() {
  if (offset) {
    url.searchParams.set('offset', offset + 1);
  } else {
    url.searchParams.set('offset', 1);
  }

  window.location = url;
})
