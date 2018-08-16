var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
var chart = new Chart(areaChartCanvas, {
  type: 'line',
  data: {},
  options: {}
});
loadContainers();

$('.js-category').click(function (e) {
  var categoryTitle = $(e.target).text();
  $('.js-category-title').text(categoryTitle);

  var categoryId = $(e.target).data('categoryId');
  if (categoryId === 0) {
    localStorage.removeItem('category_id');
  }
  else {
    localStorage.setItem('category_id', categoryId);
  }
  loadContainers();
});

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

function getParameters() {
  var params = '?';
  if (localStorage.getItem('show_by') != null) {
    params += 'show_by=' + localStorage.getItem('show_by') + '&';
  }
  if (localStorage.getItem('category_id') != null) {
    params += 'category_id=' + localStorage.getItem('category_id') + '&';
  }
  if (localStorage.getItem('offset') != null) {
    params += 'offset=' + localStorage.getItem('offset') + '&';
  }
  if (localStorage.getItem('word') != null) {
    params += 'word=' + localStorage.getItem('word') + '&';
  }
  if (localStorage.getItem('profile_id') != null) {
    params += 'profile_id=' + localStorage.getItem('profile_id') + '&';
  }
  if (localStorage.getItem('page') != null) {
    params += 'page=' + localStorage.getItem('page') + '&';
  } else {
    localStorage.setItem('page', 1)
    params += 'page=' + localStorage.getItem('page') + '&';
  }
  return params;
}

function loadContainers() {
  $('.side-bar').scrollTop(0);
  localStorage.setItem('page', 1);

  var params = getParameters();

  loadWordCloud(params);
  loadTopProfiles(params);
  loadChart(params);
  loadTweets(params);
}

var timeout;

$('.side-bar').bind('scroll', function() {
  clearTimeout(timeout);
  if($(this).scrollTop() + $(this).innerHeight()>=$(this)[0].scrollHeight) {
    timeout = setTimeout(function() {
      localStorage.page = Number(localStorage.page) + 1
      loadTweets(getParameters());
    }, 50);
  }
});

$(window).on("unload", function() {
  localStorage.clear();
});

