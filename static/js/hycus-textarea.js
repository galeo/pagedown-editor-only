/*This Jquery plugin is a combination of 2 other jquery plugins
1. http://plugins.jquery.com/project/TextAreaResizer
2. http://unwrongest.com/projects/elastic/

*/

/*
	jQuery TextAreaResizer plugin
	Created on 17th January 2008 by Ryan O'Dell
	Version 1.0.4

	Converted from Drupal -> textarea.js
	Found source: http://plugins.jquery.com/misc/textarea.js
	$Id: textarea.js,v 1.11.2.1 2007/04/18 02:41:19 drumm Exp $

	1.0.1 Updates to missing global 'var', added extra global variables, fixed multiple instances, improved iFrame support
	1.0.2 Updates according to textarea.focus
	1.0.3 Further updates including removing the textarea.focus and moving private variables to top
	1.0.4 Re-instated the blur/focus events, according to information supplied by dec


*/
(function($) {
	/* private variable "oHover" used to determine if you're still hovering over the same element */
	var textarea, staticOffset;  // added the var declaration for 'staticOffset' thanks to issue logged by dec.
	var iLastMousePos = 0;
	var iMin = 32;
	var grip;
	/* TextAreaResizer plugin */
	$.fn.TextAreaResizer = function() {
		return this.each(function() {
		    textarea = $(this).addClass('processed'), staticOffset = null;

			// 18-01-08 jQuery bind to pass data element rather than direct mousedown - Ryan O'Dell
		    // When wrapping the text area, work around an IE margin bug.  See:
		    // http://jaspan.com/ie-inherited-margin-bug-form-elements-and-haslayout
		    $(this).wrap('<div class="resizable-textarea"><span></span></div>')
		      .parent().append($('<div class="grippie"></div>').bind("mousedown",{el: this} , startDrag));

		    var grippie = $('div.grippie', $(this).parent())[0];
		    grippie.style.marginRight = (grippie.offsetWidth - $(this)[0].offsetWidth) +'px';

		});
	};
	/* private functions */
	function startDrag(e) {
		textarea = $(e.data.el);
		textarea.blur();
		iLastMousePos = mousePosition(e).y;
		staticOffset = textarea.height() - iLastMousePos;
		textarea.css('opacity', 0.25);
		$(document).mousemove(performDrag).mouseup(endDrag);
		return false;
	}

	function performDrag(e) {
		var iThisMousePos = mousePosition(e).y;
		var iMousePos = staticOffset + iThisMousePos;
		if (iLastMousePos >= (iThisMousePos)) {
			iMousePos -= 5;
		}
		iLastMousePos = iThisMousePos;
		iMousePos = Math.max(iMin, iMousePos);
		textarea.height(iMousePos + 'px');
		if (iMousePos < iMin) {
			endDrag(e);
		}
		return false;
	}

	function endDrag(e) {
		$(document).unbind('mousemove', performDrag).unbind('mouseup', endDrag);
		textarea.css('opacity', 1);
		textarea.focus();
		textarea = null;
		staticOffset = null;
		iLastMousePos = 0;
	}

	function mousePosition(e) {
		return { x: e.clientX + document.documentElement.scrollLeft, y: e.clientY + document.documentElement.scrollTop };
	};
})(jQuery);

(function(g){g.fn.extend({elastic:function(){var h=["paddingTop","paddingRight","paddingBottom","paddingLeft","fontSize","lineHeight","fontFamily","width","fontWeight"];return this.each(function(){function i(c,j){curratedHeight=Math.floor(parseInt(c,10));a.height()!=curratedHeight&&a.css({height:curratedHeight+"px",overflow:j})}function k(){var c=a.val().replace(/&/g,"&amp;").replace(/ /g,"&nbsp;").replace(/<|>/g,"&gt;").replace(/\n/g,"<br />"),j=b.html().replace(/<br>/ig,"<br />");if(c+"&nbsp;"!= j){b.html(c+"&nbsp;");if(Math.abs(b.height()+l-a.height())>3){c=b.height()+l;if(c>=d)i(d,"auto");else c<=e?i(e,"hidden"):i(c,"hidden")}}}if(this.type!="textarea")return false;var a=g(this),b=g("<div />").css({position:"absolute",display:"none","word-wrap":"break-word"}),l=parseInt(a.css("line-height"),10)||parseInt(a.css("font-size"),"10"),e=parseInt(a.css("height"),10)||l*3,d=parseInt(a.css("max-height"),10)||Number.MAX_VALUE,f=0;if(d<0)d=Number.MAX_VALUE;b.appendTo(a.parent());for(f=h.length;f--;)b.css(h[f].toString(), a.css(h[f].toString()));a.css({overflow:"hidden"});a.bind("keyup change cut paste",function(){k()});a.bind("blur",function(){if(b.height()<d)b.height()>e?a.height(b.height()):a.height(e)});a.live("input paste",function(){setTimeout(k,250)});k()})}})})(jQuery);

$.fn.hycustextarea = (function ()
{
	$(this).elastic();
	$(this).TextAreaResizer();

});