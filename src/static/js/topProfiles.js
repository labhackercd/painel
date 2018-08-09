function loadTopProfiles() {
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
  showLoader('top-profile-loader');
  $.getJSON('/top-profiles' + param, function(data) {
    var topProfiles = $('.js-top-profiles');
    topProfiles.html('');
    if (data.length) {
      $.each(data, function(i, d) {
        var element = createProfileCard(d, 'top');
        element.click({tweets: d.tweets, sectionName: 'top'}, profileHandleClick);
        topProfiles.append(element);
      })
    } else {
      topProfiles.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    showInfoContainerProfiles('top');
    hideLoader('top-profile-loader');
  });
};
