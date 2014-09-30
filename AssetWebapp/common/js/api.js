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
	$.api = function(options)
	{
		$.fn.loading.show();
		if(typeof options.url ==='undefined')
		{
			options.error.call(this,{error:'Function must define'});
			return;
		}
		
		if(typeof options.params ==='undefined')
			params = {};
		
		var posting = $.post(options.url,options.params);
		
		posting.done(function(data) 
		{
			if(typeof data.error === 'undefined')
				options.success.call(this,data);
			else
			{
				options.error.call(this,{error:data.error});
			}
			$.fn.loading.hide();
		});
		
		posting.fail(function(jqXHR, textStatus)
		{
			options.error.call(this,{error:textStatus});
			$.fn.loading.hide();
		});
	};
})(jQuery);