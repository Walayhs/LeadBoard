(function($) {
    'use strict';
    
    var $banner = $('section.interactive');
    if ($banner.length) {
        var $patterns = $banner.find('.pattern');
        
        var x = 0,
            y = 0;
        
        // Bind animation to cursor
        $(window).on('mousemove', function(event) {
            x = event.pageX;
            y = event.pageY;
        });
        
        /**
         * Tell the browser that we wish to perform an animation
         * @see https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
         */
        window.requestAnimationFrame(function animation() {

            // Loop each pattern layer
            $patterns.each(function(key) {

                // Modify the x,y coords per element to give "depth"
                var modifier = 100 * (key + 1);

                // Move background position
                $(this).css({
                    'transform': 'translate('+(x / modifier)+'px, '+(y / modifier)+'px)'
                });

            });
            
            window.requestAnimationFrame(animation);

        });
        
        
    }
    
})(jQuery);
