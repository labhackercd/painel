function loadTweets(params) {
  showLoader('top-publications-loader');
  $.getJSON('/tweets' + params, function(data) {
    var tweets = $('.js-top-publications');
    if (localStorage.page == 1) {
      tweets.html('');
    }
    if (data.length) {
        $.each(data, function(i, d) {
          tweets.append(createTweetCard(d));
        })
    } else {
      tweets.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }
  });
  hideLoader('top-publications-loader');
};