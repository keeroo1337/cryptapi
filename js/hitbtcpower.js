$(document).ready(function(){
	$.post("/cgi-bin/main.py", function( data ) {
	  	$("#content").append(data);

		$(".tablesorter").css("display", "table");
		$(".tablesorter").css("table-layout", "fixed");
		$(".tablesorter").css("border-spacing", "0px");
		$(".tablesorter").tablesorter();
		$(".tablesorter").css("width", "300px");
		$(".tablesorter").css("display", "table-cell");


	});

});