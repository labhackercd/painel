var url = new URL(window.location.href);
var param = '?' + url.searchParams.toString();

$.getJSON('/top-profiles' + param, function(data) {
  var topProfiles = $('.js-top-profiles');

  $.each(data, function(i, d) {
    var element = createProfileCard(d, 'top');
    element.click({tweets: d.tweets, sectionName: 'top'}, profileHandleClick);
    topProfiles.append(element);
  })

  showInfoContainerProfiles('top');
});
