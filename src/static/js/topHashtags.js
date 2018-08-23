var hashtagsRequest = null;
function loadTopHashtags(params) {
  hashtagsRequest = $.ajax({
    dataType: "json",
    url: '/top-hashtags',
    data: params,
    beforeSend : function() {
      showLoader('top-hashtags-loader');
      if(hashtagsRequest != null) {
        hashtagsRequest.abort();
      }
    },
  }).done(function(data) {
    var topHashtags = $('.js-top-hashtags');
    topHashtags.html('');
    if (data.length) {
      $.each(data, function(i, data) {
        var element = `
          <div class="item" data-tippy-placement="top" data-tippy="" title="${data.retweets} retweets">
            <div class="bar">
              <span class="hashtag">#${data.text}</span>
              <div class="value" style="width: ${data.value}%"></div>
            </div>
          </div>
        `
        var element = $(element)
        var elementTippy = tippy.one(element[0], {
          arrow: true,
          arrowType: 'round',
          size: 'large',
          duration: 300,
          animation: 'scale',
          placement: 'top-start',
          interactive: false,
          multiple: false,
          livePlacement: true,
          updateDuration: 350,
          createPopperInstanceOnInit: false,
          followCursor: true
        });
        element.click({hashtag: data.text}, function(e) {
          localStorage.setItem('hashtag', e.data['hashtag']);
          addFilterTag('blue', 'hashtag', '#' + e.data['hashtag']);
          elementTippy.hide();
          elementTippy.destroy();
          loadContainers();

          return false;
        });
        topHashtags.append(element);
      })
    } else {
      topHashtags.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    hideLoader('top-hashtags-loader');
    hashtagsRequest = null;
  });
};
