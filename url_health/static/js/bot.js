var casper = require('casper').create();
var urls;
var HOST = 'http://' + casper.cli.get(0) + '/';

casper.start();

casper.then(function() {
  this.open(HOST + 'url_health/fetch-links/', {
    method: 'get',
    headers: {
      'Accept': 'application/json'
      }
    })
  .then(function() {
    urls = JSON.parse(this.getPageContent()).links;
  })
});

casper.thenOpen(HOST,function() {
  casper.eachThen(urls, function(response) {
    this.thenOpen(response.data, function(response) {
      casper.open(HOST + 'url_health/post-link-info/', {
        method: 'post',
        data:   {
          'link': response.url,
          'status':  response.status
        }
    });
    });
  });
});

casper.run(function() {
  this.exit();
});