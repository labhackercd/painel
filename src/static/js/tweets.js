var tweetsRequest = null;
function loadTweets(params) {
  tweetsRequest = $.ajax({
    dataType: "json",
    url: '/tweets',
    data: params,
    beforeSend : function() {
      // showLoader('top-publications-loader');
      if(tweetsRequest != null) {
        tweetsRequest.abort();
      }
    },
  }).done(function(data) {
    var tweets = $('.js-top-publications');
    if (localStorage.page == 1) {
      tweets.html('');
    }
    if (data.length) {
        $.each(data, function(i, d) {
          var element = createTweetCard(d);
          element.click({tweet_id: d.tweet_id_str}, tweetHandleClick);
          tweets.append(element);
        })
    } else {
      tweets.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }
    tweetsRequest = null;
    // hideLoader('top-publications-loader');
  });
};