function getNumPage() {
  var location = window.location.search;
  var p = location.split('&');
  var query_string = new Object();

  for (var i=0;i<p.length;i++) {
    var pair = p[i].split("=");
    query_string[pair[0]] = pair[1];
  }

  return query_string["page"]
}

// Store what page to load next
var nextpage = parseInt(getNumPage()) ? (parseInt(getNumPage()) + 1) : 2;
// var nextpage = parseInt(getNumPage());

$('#load_more').click(function(event) {
  // Retains compatibility for those with no javascript
  event.preventDefault();

  // Fetch the data
  //$.get('/ajax.php?page=' + nextpage, function(html){
  var addrOfSite = window.location.href
  var subAddr = '';
  var order_by = addrOfSite.search('&order_by')

  if ( order_by != -1 ) {
  	subAddr = addrOfSite.substring(order_by, addrOfSite.length);
  }

  $.get('/?page=' + nextpage + subAddr, function(data){
    // Put the data where it belongs. I like it more this way
    var path = $(data).find('tbody');
    // alert(path.children().text());
    $('tbody').append(path.children());
    //$( path ).insertAfter( "div#testframe" );

    // Keep the counter up-to-date
    nextpage++;
    });
  });
