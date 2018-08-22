function loadTopProfiles(params) {
  var profilesRequest = $.ajax({
    dataType: "json",
    url: '/top-profiles',
    data: params,
    beforeSend : function() {
      showLoader('main-influencers-loader');
      if(profilesRequest != null) {
        profilesRequest.abort();
      }
    },
  }).done(function(data) {
    var topProfiles = $('.js-top-profiles');
    topProfiles.html('');
    if (data.length) {
      var max_engagement = data[0].engagement
      $.each(data, function(i, d) {
        var element = createProfileCard(d, max_engagement);
        element.click({profile_id: d.id, name: d.name}, profileHandleClick);
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

    hideLoader('main-influencers-loader');
  });
};
