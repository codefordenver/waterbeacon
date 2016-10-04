var $ = django.jQuery;
$(function(){

$('#id_sourcetype').change(function(){
    //do something on select change
    if($('option:selected',this).text() == "simulator"){
    	$(".field-commtype").hide()
    	$(".field-deviceaddress").hide()
    	$(".field-hostip").hide()
    	$(".field-proxy_url").hide()
    }else{
    	$(".field-commtype").show()
    	$(".field-deviceaddress").show()
    	$(".field-hostip").show()
    	$(".field-proxy_url").show()
    }

    });

	$(".field-commtype").hide()
	$(".field-deviceaddress").hide()
	$(".field-hostip").hide()
	$(".field-proxy_url").hide()

});
