$("#search").keyup(function() {
    var value = this.value.toLowerCase().trim();

    $("table").find("tr").each(function(index) {
        if (index === 0) return;

        var if_td_has = false;
        $(this).find('td').each(function () {
            if_td_has = if_td_has || $(this).text().toLowerCase().trim().indexOf(value) !== -1;
        });

        $(this).toggle(if_td_has);

    });
});

$('.item')
  .popup({
  	position : 'bottom center'
  })
;