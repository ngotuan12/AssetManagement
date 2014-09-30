/**
 * @author TuanNA 
 * @since 29/09/2014
 * @version 1.0
 * @require 
 *   jquery
 *   boostrap
 *   loadding.js
 *   error.js
 * Get data from API
 *
 * Copyright (c) 2014, Ngo Anh Tuan
 * 
 */
(function($)
{
	/**
	 * @param 
	 * 	url require
	 *  params:
	 *    http request parameter
	 *    type: Array
	 *  onSuccess:
	 *    function
	 *  onError:
	 *    function
	 */
	$.api = function(url,params,onSuccess,onError)
	{
		var posting = $.post(url,params);
		posting.done(function(data) {
			if(typeof data.error === 'undefined')
				onSuccess.call(this,data);
			else
				onError.call(this,data);
		});
		posting.fail(function(jqXHR, textStatus)
		{
			
			data = {};
			data.error = textStatus;
			onError.call(this,data);
		});
	};
})(jQuery);