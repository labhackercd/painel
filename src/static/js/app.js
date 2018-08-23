var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
var chart = new Chart(areaChartCanvas, {
  type: 'line',
  data: {},
  options: {}
});
loadContainers();

$('.js-category').click(function (e) {
  var categoryTitle = $(e.target).text();
  var title = $('.js-category-title').get(0);

  var text_to_change = title.childNodes[0];

  text_to_change.nodeValue = categoryTitle;

  var categoryId = $(e.target).data('categoryId');
  if (categoryId === 0) {
    localStorage.removeItem('category_id');
  }
  else {
    localStorage.setItem('category_id', categoryId);
  }
  loadContainers();
});

$('.js-filter-buttons a').click(function() {
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
};

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
});

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
});

function getParameters() {
  params = Object.keys(localStorage).reduce(function(obj, str) {
    obj[str] = localStorage.getItem(str);
    return obj
  }, {});
   return params
};

function addFilterTag (color, filterType, tagName, filterValue) {
  var tags = $(".js-tag").map(function (idx, ele) {
   return $(ele).data('filterType');
  }).get();
  if (filterType === 'word') {
    var append = true;
    var currentWord = localStorage.getItem('word');
    if (currentWord) {
      var currentWordArray = currentWord.split(',');
      if (currentWordArray.indexOf(filterValue) >= 0) {
        append = false
      }
    }
    if (append) {
      $('.js-filter-tags').append(`
        <div class="tag -${color} js-tag" data-filter-type="${filterType}" data-filter-value="${filterValue}">
          <i class="fas fa-times"></i>${tagName}
        </div>
      `);
    } else {
      return false;
    }
  } else if (tags.indexOf(filterType) < 0) {
    $('.js-filter-tags').append(`
      <div class="tag -${color} js-tag" data-filter-type="${filterType}">
        <i class="fas fa-times"></i>${tagName}
      </div>
    `);
  } else {
    return false;
  }
};

function store(key, value) {
  var currentValue = localStorage.getItem(key);
  if (currentValue) {
    var currentArray = currentValue.split(',');
    var i = currentArray.indexOf(value);
    if (i < 0) {
      currentArray = currentArray.concat(value);
      localStorage.setItem(key, currentArray);
    }
  } else {
    localStorage.setItem(key, value);
  }
}

function popFromStorage(key, value) {
  var currentValue = localStorage.getItem(key);
  if (currentValue) {
    var currentArray = currentValue.split(',')
    var i = currentArray.indexOf(value);
    if (i >= 0) {
      currentArray.splice(i, 1);
      localStorage.setItem(key, currentArray);
    }
  }
}

$('.js-filter-tags').on("click", ".js-tag", function() {
  if ($(this).data('filterType') === 'word') {
    popFromStorage('word', $(this).data('filterValue'));
  } else {
    localStorage.removeItem($(this).data('filterType'))
  }
  $(this).remove();
  loadContainers();
});

$('.js-clean-filters').on("click", function() {
  var filters = ['hashtag', 'profile_id', 'mentioned_id', 'link', 'word'];

  $(filters).each(function(i, key){
    localStorage.removeItem(key);
  });
  $('.js-tag').remove();
  loadContainers();
});

function loadContainers() {
  $('.js-scroll-tweets').scrollTop(0);
  localStorage.setItem('page', 1);

  var filters = ['hashtag', 'profile_id', 'mentioned_id', 'link', 'word'];
  var params = getParameters();
  var resultList = filters.filter(value => -1 !== Object.keys(params).indexOf(value));

  if (resultList.length >= 1) {
    $('.js-filter-tags').addClass('-show');
    $('.js-nav-menu, .js-filter-tags').addClass('-translated');

  } else {
    $('.js-filter-tags').removeClass('-show');
    $('.js-nav-menu, .js-filter-tags').removeClass('-translated');
  }

  loadWordCloud(params);
  loadTopProfiles(params);
  loadTopMentions(params);
  loadTopHashtags(params);
  loadTopLinks(params);
  loadChart(params);
  loadTweets(params);
};

var timeout;

$('.js-scroll-tweets').on('scroll', function() {
  clearTimeout(timeout);
  if(Math.round($(this).scrollTop() + $(this).innerHeight()) >= $(this)[0].scrollHeight) {
    timeout = setTimeout(function() {
      localStorage.page = Number(localStorage.page) + 1
      loadTweets(getParameters());
    }, 50);
  }
});

$(window).on("unload", function() {
  localStorage.clear();
});
