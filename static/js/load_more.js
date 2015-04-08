// Store what page to load next
nextpage = 2;

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
    startPath = data.search("<!-- Start Add more students -->");
    endPath = data.search("<!-- Add more students -->");
    path = data.substring(startPath,endPath);
    //alert(path);
    $("div#testframe").append(path);
    //$( path ).insertAfter( "div#testframe" );

    // Keep the counter up-to-date
    nextpage++;
    });
  });
