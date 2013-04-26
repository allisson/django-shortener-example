/**
 * jQuery.ScrollTo - Easy element scrolling using jQuery.
 * Copyright (c) 2007-2009 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
 * Dual licensed under MIT and GPL.
 * Date: 5/25/2009
 * @author Ariel Flesler
 * @version 1.4.2
 *
 * http://flesler.blogspot.com/2007/10/jqueryscrollto.html
 */
;(function(d){var k=d.scrollTo=function(a,i,e){d(window).scrollTo(a,i,e)};k.defaults={axis:'xy',duration:parseFloat(d.fn.jquery)>=1.3?0:1};k.window=function(a){return d(window)._scrollable()};d.fn._scrollable=function(){return this.map(function(){var a=this,i=!a.nodeName||d.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!i)return a;var e=(a.contentWindow||a).document||a.ownerDocument||a;return d.browser.safari||e.compatMode=='BackCompat'?e.body:e.documentElement})};d.fn.scrollTo=function(n,j,b){if(typeof j=='object'){b=j;j=0}if(typeof b=='function')b={onAfter:b};if(n=='max')n=9e9;b=d.extend({},k.defaults,b);j=j||b.speed||b.duration;b.queue=b.queue&&b.axis.length>1;if(b.queue)j/=2;b.offset=p(b.offset);b.over=p(b.over);return this._scrollable().each(function(){var q=this,r=d(q),f=n,s,g={},u=r.is('html,body');switch(typeof f){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(f)){f=p(f);break}f=d(f,this);case'object':if(f.is||f.style)s=(f=d(f)).offset()}d.each(b.axis.split(''),function(a,i){var e=i=='x'?'Left':'Top',h=e.toLowerCase(),c='scroll'+e,l=q[c],m=k.max(q,i);if(s){g[c]=s[h]+(u?0:l-r.offset()[h]);if(b.margin){g[c]-=parseInt(f.css('margin'+e))||0;g[c]-=parseInt(f.css('border'+e+'Width'))||0}g[c]+=b.offset[h]||0;if(b.over[h])g[c]+=f[i=='x'?'width':'height']()*b.over[h]}else{var o=f[h];g[c]=o.slice&&o.slice(-1)=='%'?parseFloat(o)/100*m:o}if(/^\d+$/.test(g[c]))g[c]=g[c]<=0?0:Math.min(g[c],m);if(!a&&b.queue){if(l!=g[c])t(b.onAfterFirst);delete g[c]}});t(b.onAfter);function t(a){r.animate(g,j,b.easing,a&&function(){a.call(this,n,b)})}}).end()};k.max=function(a,i){var e=i=='x'?'Width':'Height',h='scroll'+e;if(!d(a).is('html,body'))return a[h]-d(a)[e.toLowerCase()]();var c='client'+e,l=a.ownerDocument.documentElement,m=a.ownerDocument.body;return Math.max(l[h],m[h])-Math.min(l[c],m[c])};function p(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);

AJS.$(document).ready(function(){

    // Quick version awareness, to avoid having to double-process the soy.
    AJS.$("#indexheader").append('<span class="aui-lozenge aui-lozenge-current">' + AJS.version + '</span>');
    AJS.$("#aui-footer-list").append("<li>Version: " + AJS.version + "</li>");

    var nav = AJS.$("#all-in-nav"),
        navMenu = AJS.$('<ul class="jumplinks"><li>Quick jump</li></ul>'),
        headings = AJS.$('#content .aui-page-panel-content > h2');
    
    headings.each( function(index,value) {
        // quick and dirty. smashing this out, y'all.
        navMenu.append("<li><a href=\"#" + AJS.$(this).attr("id") + "\">" + AJS.$(this).text() + "</a></li>");
    });
    nav.append("<h2>Contents</h2>");
    nav.append(navMenu);

    AJS.$("#all-in-nav").delegate("a", "click", function (e) {
        var $a = AJS.$(this);
        e.preventDefault();
        AJS.$.scrollTo($a.attr("href"), 200, { easing: 'swing' });
    });


    AJS.$("#dropDown-standard").dropDown("Standard", {alignment: "left"});

    //AJS.InlineDialog(AJS.$("#popupLink"), 1, "inline-dialog-content.html");

    AJS.InlineDialog(AJS.$("#popupLink"), 1, 
        function(content, trigger, showPopup) {
            content.css({"padding":"16px"}).html('<p>Appended content.</p>');
            showPopup();
            return false;
        }
    );

    // create a dialog 860px wide x 530px high
    var dialog = new AJS.Dialog({width:860, height:530, id:"example-dialog", closeOnOutsideClick: true});
    
    // PAGE 0 (first page)
    // adds header for first page
    dialog.addHeader("Dialog - Page 0");
    
    // add panel 1
    dialog.addPanel("Panel 1", "<p>Some content for panel 1. This has no padding.</p>", "panel-body");
    dialog.get("panel:0").setPadding(0);
    
    // add panel 2 (this will create a menu on the left side for selecting panels within page 0)
    dialog.addPanel("Panel 2", "<p>Some content for panel 2.</p><div style=\"height: 2000px;\">(forced-height element to demonstrate scrolling content)</div><p>End.</p>", "panel-body");
    
    dialog.addButton("Next", function (dialog) {
        dialog.nextPage();
    });
    dialog.addButton("Cancel", function (dialog) {
        dialog.hide();
    });
    
    // PAGE 1 (second page)
    // adds a new page to dialog
    dialog.addPage();
    
    // adds header for second page
    dialog.addHeader("Dialog - Page 1");
    
    // adds a single panel on second page (as there is only one panel, no menu will appear on the left side)
    dialog.addPanel("SinglePanel", "<p>Some content for the only panel on Page 1</p>", "singlePanel");
    
    // add "Previous" button to page 1
    dialog.addButton("Previous", function(dialog) {
       dialog.prevPage();
    });
    // adds "Cancel" button to page 1
    dialog.addButton("Cancel", function (dialog) {
        dialog.hide();
    });
    
    // Add events to dialog trigger elements
    AJS.$("#dialog-button").click(function() {
        // PREPARE FOR DISPLAY
        // start first page, first panel
        dialog.gotoPage(0);
        dialog.gotoPanel(0);
        dialog.show();
    });
    
    AJS.$("#dialog-link").click(function(){
        dialog.gotoPage(0);
        dialog.gotoPanel(0);
        dialog.show(); 
    });

    AJS.messages.success({
        title: "Success!",
        body: "Created by JS with default options."
    });
    
    AJS.messages.info("#custom-context", {
        title: "Info",
        body: "You can have uncloseable messages.",
        closeable: false
    });
    
    AJS.messages.setup()
    

/**
 * Keyboard shortcuts
 */
AJS.whenIType("ze").execute(function () {
    alert("You typed z then e.");
});

/**
 * Messages example
 */
    AJS.messages.success({
        title: "Success!",
        body: "This message was created by JS with default options."
    });

/**
 * Date Picker
 */
    // AJS.$('#demo-range-always').datePicker({'overrideBrowserDefault': true});

/**
 * Dropdown1
 */
    AJS.$("#dropDown-standard").dropDown("Standard", {alignment: "right"});
    AJS.$("#demo-toolbar").dropDown("Standard", {alignment: "right"});

/**
 * Dropdown example
 */
    AJS.messages.setup()
    // create a dialog 860px wide x 530px high
    var dialog = new AJS.Dialog({width:860, height:530, id:"example-dialog", closeOnOutsideClick: true});
    
    // PAGE 0 (first page)
    // adds header for first page
    dialog.addHeader("Dialog - Page 0");
    
    // add panel 1
    dialog.addPanel("Panel 1", "<p>You can have a single panel, multiple panels, or even a wizard-style set of steps (see the button below).</p>", "panel-body");
    dialog.get("panel:0");
    
    // add panel 2 (this will create a menu on the left side for selecting panels within page 0)
    dialog.addPanel("Panel 2", "<p>Quidquid latine dictum sit, altum viditur. Sentio aliquos togatos contra me conspirare.</p>", "panel-body");
    
    dialog.addButton("Next", function (dialog) {
        dialog.nextPage();
    });
    dialog.addCancel("Cancel", function (dialog) {
        dialog.hide();
    });
    
    // PAGE 1 (second page)
    // adds a new page to dialog
    dialog.addPage();
    
    // adds header for second page
    dialog.addHeader("Dialog - Page 1");
    
    // adds a single panel on second page (as there is only one panel, no menu will appear on the left side)
    dialog.addPanel("SinglePanel", "<p>Quidquid latine dictum sit, altum viditur. Sentio aliquos togatos contra me conspirare.</p>", "singlePanel");
    
    // add "Previous" button to page 1
    dialog.addButton("Previous", function(dialog) {
       dialog.prevPage();
    });
    // adds "Cancel" button to page 1

    dialog.addCancel("Cancel", function (dialog) {
        dialog.hide();
    });
    
    // Add events to dialog trigger elements
    AJS.$("#dialog-button").click(function() {
        // PREPARE FOR DISPLAY
        // start first page, first panel
        dialog.gotoPage(0);
        dialog.gotoPanel(0);
        dialog.show();
    });
    
    AJS.$("#dialog-link").click(function(){
        dialog.gotoPage(0);
        dialog.gotoPanel(0);
        dialog.show(); 
    });

/**
 * Inline Dialog
 */
    // AJS.InlineDialog(AJS.$("#popupLink"), 1, "inline-dialog-content.html");
    AJS.InlineDialog(AJS.$("#popupLink"), 1, 
        function(content, trigger, showPopup) {
            content.css({"padding":"16px"}).html('<p>Inline dialog content.</p>');
            showPopup();
            return false;
        }
    );


/**
 * 
 */



/**
 * Preventing default for examples. Red Dwarf namespace required ;)
 */
    AJS.$("#format-dropdown").dropDown("Standard", {alignment: "left"});
    AJS.$(".example-click").click(function() {  alert('Clicked!'); return false; });
    AJS.$("#action-1a").click(function() {  alert('Clicked! The split button\'s main trigger works separately from its dropdown.'); return false; });
    AJS.$("#action-1b").dropDown("Standard", {alignment: "right"});

    AJS.$(".aui-dropdown2 a").click(function(e) {
        alert('It\'s cold outside, there\'s no kind of atmosphere,\nI\'m all alone, more or less,\nLet me fly, far away from here,\nFun, fun, fun, in the sun, sun, sun...\nI want to lie shipwrecked and comatose,\nDrinking fresh mango juice,\nGoldfish shoals, nibbling at my toes,\nFun, fun, fun, in the sun, sun, sun...\nFun, fun, fun, in the sun, sun, sun...');
        e.preventDefault();
        return false;
    });
    AJS.$(".item-link").click(function(e) {
        alert("Smoke me a kipper, I'll be back for breakfast.");
        e.preventDefault();
        return false;
    });
    AJS.$(".cancel").click(function(e) {
        alert("Rude alert! Rude alert! An electrical fire has knocked out my voice recognition unicycle! Many Wurlitzers are missing from my database. Abandon shop! This is not a daffodil. Repeat: This is not a daffodil.");
        e.preventDefault();
        return false;
    });

    AJS.$("#example").submit(function(e) {
        alert("The phrase \"open cargo bay doors\" does not appear to be in my mexican.");
        e.preventDefault();
        return false;
    });

    AJS.$(".buttons-example .aui-button:not([aria-disabled='true'])").click(function(e) {
        alert("We'll rescue these fair blooms or my name's not Captain A.J. Rimmer, Space Adventurer.");
        e.preventDefault();
        return false;
    });

    AJS.$(".buttons-example .aui-button[aria-disabled='true']").click(function(e) {
        alert("They're dead, Dave.");
        e.preventDefault();
        return false;
    });

    AJS.$(".aui-buttons .aui-button:not(.aui-dropdown2-trigger)").click( function(e){
        var pressed = AJS.$(this).attr("aria-pressed");
        if (pressed == "true") {
            AJS.$(this).attr("aria-pressed", false);
        } else {
            AJS.$(this).attr("aria-pressed", true);
        }
        return false;
    });

    AJS.$("#aui-hnav-example a, #aui-vnav-example a").click(function(e) {
        alert("When in Rome, do as the Snamor do!");
        e.preventDefault();
        return false;
    });

});


