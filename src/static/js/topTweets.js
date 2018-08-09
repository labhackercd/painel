function loadTopTweets() {
  var param = '?';
  if(localStorage.getItem('show_by') != null){
    param += 'show_by=' + localStorage.getItem('show_by') + '&';
  }
  if(localStorage.getItem('category_id') != null){
    param += 'category_id=' + localStorage.getItem('category_id') + '&';
  }
  if(localStorage.getItem('offset') != null){
    param += 'offset=' + localStorage.getItem('offset');
  }
  showLoader('top-publications-loader');
  $.getJSON('/top-tweets' + param, function(data) {
    var topTweets = $('.js-top-publications');
    topTweets.html('');
    if (data.length) {
        $.each(data, function(i, d) {
          topTweets.append(createTweetCard(d));
        })
    } else {
      topTweets.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }
    hideLoader('top-publications-loader');
  });
};