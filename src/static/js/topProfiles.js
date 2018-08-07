$.getJSON('/static/top-profiles.json', function(data) {
  var topProfiles = $('.js-top-profiles');

  $.each(data, function(i, d) {
    var element = createProfileCard(d, 'top');
    element.click({tweets: d.tweets, sectionName: 'top'}, profileHandleClick);
    topProfiles.append(element);
  })

  showInfoContainerProfiles('top');
});
