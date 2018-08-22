var mentionsRequest = null;
function loadTopMentions(params) {
  mentionsRequest = $.ajax({
    dataType: "json",
    url: '/top-mentions',
    data: params,
    beforeSend : function() {
      showLoader('top-mentions-loader');
      if(mentionsRequest != null) {
        mentionsRequest.abort();
      }
    },
  }).done(function(data) {
    var topMentions = $('.js-top-mentions');
    topMentions.html('');
    if (data.length) {
      $.each(data, function(i, data) {
        var element = `
          <div class="item" data-tippy-placement="top" data-tippy="" title="@${data.screen_name}">
            <img src="https://avatars.io/twitter/${data.screen_name}" alt="profile image">
            <span class="value">${data.retweets}</span>
            <span>Tweets</span>
          </div>
        `
        var element = $(element);
        var elementTippy = tippy.one(element[0], {
          arrow: true,
          arrowType: 'round',
          size: 'large',
          duration: 300,
          animation: 'scale',
          placement: 'top-start',
          interactive: false,
          multiple: false,
          createPopperInstanceOnInit: false,
          followCursor: true
        });
        element.click({mentioned_id: data.id, screen_name: data.screen_name}, function(e) {
          localStorage.setItem('mentioned_id', e.data['mentioned_id']);
          addFilterTag('orange', 'mentioned_id', '@' + e.data['screen_name']);
          elementTippy.hide();
          elementTippy.destroy();
          loadContainers();

          return false;
        });
        topMentions.append(element);
      })
    } else {
      topMentions.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }
    hideLoader('top-mentions-loader');
    mentionsRequest = null;
  });
};
